import subprocess, json
from typing import Any
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from datetime import datetime, timezone


class Lighthouse:
    
    def __init__(self) -> None:
        pass

    def _safe_metric(self, audits: dict, key: str) -> float | None:
        """
        Безопасно достаёт numericValue из аудита Lighthouse.
        Возвращает float или None, если метрика отсутствует/битая.
        """
        metric = audits.get(key)
        if not metric:
            return None

        value = metric.get("numericValue")
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @retry(
        stop=stop_after_attempt(3),               # максимум 3 попытки
        wait=wait_fixed(2),                       # между ними 2 секунды пауза
        retry=retry_if_exception_type(            # ретраим только на этих типах ошибок
            (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError)
        )
    )
    def _run_once(self, cmd: list[str], timeout_sec: int) -> dict[str, Any]:
        """Одиночный запуск lighthouse (с ретраями от tenacity)."""
        lighthouse_stats = subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=timeout_sec
        )
        return json.loads(lighthouse_stats.stdout)

    def run(
        self,
        url: str,
        timeout_sec: int = 240,
        header: bool = False,
        path_to_header_json: str = "headers.json",
    ) -> dict[str, Any]:
        """
        Запускает команду lighthouse для получения статистики

        Args:
            url(str): ссылка на ресурс
            timeout_sec(int): таймаут для команды в секундах
            header(bool): отправлять или не отправлять header. (Может вляиять на lighthouse статистику)
            path_to_header_json(str):
        Returns:
            dict: json ответ lighthouse с статистикой.
                - Если произойдет какая либо ошибка - вернет валидный JSON с ошибкой
                - Пример возвращаемого JSON:
                    {
                        "status": "success",
                        "url": "https://example.com",
                        "metrics": {
                            "fcp_ms": 1234.56,
                            "fcp_s": 1.23,
                            "tbt_ms": 50.12,
                            "tbt_s": 0.05,
                            "si_ms": 1800.01,
                            "si_s": 1.8,
                            "lcp_ms": 2345.67,
                            "lcp_s": 2.35,
                            "cls": 0.05
                        }
                    }
                * fcp → First Contentful Paint(в млс и сек)
                * tbt → Total Blocking Time (в млс и сек)
                * si → Speed Index (в млс и сек)
                * lcp → Largest Contentful Paint (в млс и сек)
                * cls → Cumulative Layout Shift
        """
        # _____________________________________________________Пояснялка к команде:
        # --quiet -→ что бы не сам lighthouse не срал в консоль
        # --chrome-flags= --headless -→ что бы не запускал окно браузера
        # --chrome-flags= --disable-cache -→ явно указываем что бы запрос был без кэша
        # --output=json -→ вывод в json (по дефлоту HTML)
        # --output-path=stdout -→ что бы возвращал json в консоль subprocess (по дефолту в файл)
        # --only-audits=first-contentful-paint,... -→ что бы гонял только нужные метрики, иначе будет в stdout срать json'ом в несколько мегабайт

        # До кучи можно прописать --disable-storage-reset=false что бы Lighthouse сам всегда 
        # сбрасывал localStorage, IndexedDB, кеш 
        # и прочее добро, прежде чем прогнать аудит, 
        # но я не стал играться так как по идее он это делает по дефолту
        
        # _____________________________________________________
        # Если будут ошибки аля "No usable sandbox!" нужно:
        # К --chrome-flags добавить → --no-sandbox

        # Возможно будут ошибки из за отсутсвия GPU:
        # Если будут к --chrome-flags добавить → --disable-gpu
        base_cmd = [
            "lighthouse",
            url,
            "--quiet",
            "--chrome-flags=--headless --disable-cache",
            "--output=json",
            "--output-path=stdout",
            "--only-audits=first-contentful-paint,total-blocking-time,speed-index,largest-contentful-paint,cumulative-layout-shift",
        ]

        if header:
            base_cmd.append(f"--extra-headers={path_to_header_json}")

        try:
            data = self._run_once(base_cmd, timeout_sec)

            metrics = {
                "fcp_ms": (fcb := self._safe_metric(data["audits"], "first-contentful-paint")),
                "fcp_s": round(fcb / 1000, 2) if fcb is not None else None,
                "tbt_ms": (tbt := self._safe_metric(data["audits"], "total-blocking-time")),
                "tbt_s": round(tbt / 1000, 2) if tbt is not None else None,
                "si_ms": (si := self._safe_metric(data["audits"], "speed-index")),
                "si_s": round(si / 1000, 2) if si is not None else None,
                "lcp_ms": (lcp := self._safe_metric(data["audits"], "largest-contentful-paint")),
                "lcp_s": round(lcp / 1000, 2) if lcp is not None else None,
                "cls": self._safe_metric(data["audits"], "cumulative-layout-shift"),
            }

            return {
                "@timestamp" : datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"), # время в формате 2025-10-02T18:10:45.940Z для елки
                "status": "success",
                "url": url,
                "metrics": metrics,
                "error": None,
                "message": None,
            }

        except subprocess.CalledProcessError as eCPE:
            return {
                "url": url,
                "status": "error",
                "metrics": None,
                "error": "Lighthouse failed",
                "message": f"stderr: {eCPE.stderr.strip()[:500]} | stdout: {eCPE.stdout.strip()[:500]}",
            }
        except subprocess.TimeoutExpired as eTE:
            return {
                "url": url,
                "status": "error",
                "metrics": None,
                "error": "Lighthouse timeout",
                "message": str(eTE),
            }
        except FileNotFoundError as eFNF:
            return {
                "url": url,
                "status": "error",
                "metrics": None,
                "error": "Lighthouse binary not found",
                "message": str(eFNF),
            }
        except json.JSONDecodeError as eJSDE:
            return {
                "url": url,
                "status": "error",
                "metrics": None,
                "error": "Invalid JSON from Lighthouse",
                "message": str(eJSDE),
            }
        except Exception as e:
            return {
                "url": url,
                "status": "error",
                "metrics": None,
                "error": "Unexpected exception",
                "message": str(e),
            }

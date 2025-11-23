import docker
import os
import sys
import subprocess


class DockerMonitor:

    def __init__(self):
        self.client = self._connect_to_docker()

    def _connect_to_docker(self):
        """
        Attempt to connect to Docker daemon using multiple strategies.
        Last Resort: Ask the docker CLI where the socket is.
        """
        try:
            client = docker.from_env()
            client.ping()
            return client
        except Exception:
            pass

        possible_urls = []

        if sys.platform.startswith("win"):
            possible_urls.append("npipe:////./pipe/docker_engine")
        else:
            # Unix/Mac Standard
            possible_urls.append("unix:///var/run/docker.sock")
            # Mac Docker Desktop (User Home)
            possible_urls.append(f"unix://{os.path.expanduser('~')}/.docker/run/docker.sock")
            # Mac Docker Desktop (Alternative)
            possible_urls.append(f"unix://{os.path.expanduser('~')}/.docker/desktop/docker.sock")

        try:
            # Run command to find the host endpoint
            cmd = "docker context inspect --format '{{.Endpoints.docker.Host}}'"
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if result:
                possible_urls.append(result)
        except Exception:
            pass

        last_error = None

        for url in possible_urls:
            try:
                url = url.strip("'").strip('"')

                client = docker.DockerClient(base_url=url)
                client.ping()
                return client
            except Exception as e:
                last_error = e
                continue

        raise Exception(
            f"Could not connect to Docker. \n"
            f"Tried paths: {possible_urls}. \n"
            f"Last error: {last_error}"
        )

    def calculate_cpu_percent(self, stats):
        """Calculate CPU usage percentage."""
        cpu_count = len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", []))
        if cpu_count == 0:
            cpu_count = stats["cpu_stats"].get("online_cpus", 1)

        cpu_delta = float(stats["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                    float(stats["precpu_stats"]["cpu_usage"]["total_usage"])
        system_delta = float(stats["cpu_stats"]["system_cpu_usage"]) - \
                       float(stats["precpu_stats"]["system_cpu_usage"])

        if system_delta > 0.0 and cpu_delta > 0.0:
            cpu_percent = (cpu_delta / system_delta) * cpu_count * 100.0
            return round(cpu_percent, 2)
        return 0.0

    def calculate_mem_percent(self, stats):
        """Calculate memory usage percentage."""
        usage = stats["memory_stats"].get("usage", 0)
        limit = stats["memory_stats"].get("limit", 1)
        if limit > 0:
            return round((usage / limit) * 100.0, 2)
        return 0.0

    def bytes_to_mb(self, size_in_bytes):
        return round(size_in_bytes / (1024 * 1024), 2)

    def get_all_stats(self):
        """Get a snapshot of statistics for all running containers."""
        results = []
        try:
            containers = self.client.containers.list()
        except Exception:
            return []

        for container in containers:
            try:
                stats = container.stats(stream=False)
                cpu_pct = self.calculate_cpu_percent(stats)
                mem_pct = self.calculate_mem_percent(stats)
                mem_usage = self.bytes_to_mb(stats["memory_stats"].get("usage", 0))
                mem_limit = self.bytes_to_mb(stats["memory_stats"].get("limit", 0))

                results.append({
                    "id": container.short_id,
                    "name": container.name,
                    "status": container.status,
                    "cpu": f"{cpu_pct}%",
                    "memory": f"{mem_usage}MB / {mem_limit}MB ({mem_pct}%)"
                })
            except Exception:
                continue
        return results

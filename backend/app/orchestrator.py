import docker
import random
import time
from datetime import datetime

class ClusterManager:
    def __init__(self):
        self.client = docker.from_env()
        self.event_log = []
        self.chaos_mode = True 
        self.add_log("System", "Orchestrator Online. Auto-Recovery Subsystems: ACTIVE.")

    def add_log(self, source, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.insert(0, {"time": timestamp, "source": source, "msg": message})
        if len(self.event_log) > 50:
            self.event_log.pop()

    # --- ELASTIC SCALING PROTOCOLS ---
    def spawn_node(self):
        try:
            existing = self.client.containers.list(all=True, filters={"name": "worker"})
            # Unique naming convention for dynamic nodes
            node_name = f"worker-dynamic-{len(existing)+1}-{random.randint(1000,9999)}"
            
            self.client.containers.run(
                "alpine",
                'sh -c "while true; do sleep 1000; done"',
                detach=True,
                name=node_name,
                network="sentinellus_default",
                mem_limit="512m" # Resource limiting for realism
            )
            self.add_log("AutoScaler", f"PROVISIONED new capacity: {node_name}")
            return True
        except Exception as e:
            self.add_log("Error", f"Provisioning Failed: {str(e)}")
            return False

    def remove_node(self):
        try:
            # Find all dynamic nodes (avoid killing the base 3 static ones if possible, or just kill last)
            containers = self.client.containers.list(all=True, filters={"name": "worker"})
            if not containers:
                return False
            
            # Decommission the newest node (Last In, First Out)
            # We sort by creation time usually, but for simple demo, just picking the last in list is fine
            target = containers[0] # List often returns newest first, or we pick one.
            name = target.name
            
            target.stop()
            target.remove()
            
            self.add_log("AutoScaler", f"DECOMMISSIONED node: {name} (Scale Down)")
            return True
        except Exception as e:
            self.add_log("Error", f"Decommission Failed: {str(e)}")
            return False

    def get_system_health(self):
        containers = self.client.containers.list(all=True, filters={"name": "worker"})
        
        # 1. Traffic Logic
        base_traffic = random.randint(3000, 7000)
        healthy_nodes = [c for c in containers if c.status == "running"]
        active_count = len(healthy_nodes)
        
        data = []
        total_latency = 0
        overloaded_count = 0

        for c in containers:
            is_alive = c.status == "running"
            node_status = "CRITICAL"
            error_msg = "NONE"
            simulated_cpu = 0
            latency = 0
            
            # 2. CHAOS MONKEY (The "King" Logic)
            # 10% chance to kill a node if we have more than 3 (don't kill if we are low on nodes)
            if is_alive and self.chaos_mode and active_count > 3 and random.random() < 0.05:
                print(f"😈 Chaos Monkey executing {c.name}")
                try:
                    c.kill()
                    is_alive = False
                    self.add_log("ChaosEngine", f"Randomly terminated {c.name}")
                except:
                    pass

            if not is_alive:
                try:
                    exit_code = c.attrs['State']['ExitCode']
                    error_msg = "FATAL_EXCEPTION" if exit_code == 137 else "SYSTEM_CRASH"
                except:
                    error_msg = "UNKNOWN_FAILURE"
                node_status = "CRITICAL"
            else:
                # Real Load Logic
                traffic_share = int(base_traffic / active_count) if active_count else 0
                simulated_cpu = min(99, int((traffic_share / 1000) * 100) + random.randint(-5, 5))
                latency = int((simulated_cpu * 1.5) + random.randint(10, 50))

                if simulated_cpu > 90:
                    node_status = "OVERLOADED"
                    overloaded_count += 1
                elif simulated_cpu > 75:
                    node_status = "WARNING"
                else:
                    node_status = "HEALTHY"

            if is_alive:
                total_latency += latency

            data.append({
                "id": c.short_id,
                "name": c.name,
                "status": node_status,
                "error": error_msg,
                "cpu": simulated_cpu,
                "memory": random.randint(200, 800) if is_alive else 0,
                "requests_per_sec": traffic_share if is_alive else 0,
                "latency": latency
            })

        # Smart Health Score
        total_nodes = len(containers)
        health_score = 0
        if total_nodes > 0:
            penalty = ((total_nodes - active_count) * 20) + (overloaded_count * 5)
            health_score = max(0, 100 - penalty)

        avg_latency = int(total_latency / active_count) if active_count > 0 else 0

        return {
            "nodes": data,
            "events": self.event_log,
            "total_traffic": base_traffic,
            "avg_latency": avg_latency,
            "health_score": health_score,
            "stress_mode": False
        }

    def heal_node(self, container_id):
        time.sleep(1) # Realistic recovery delay
        try:
            container = self.client.containers.get(container_id)
            container.restart()
            self.add_log("Orchestrator", f"RECOVERY PROTOCOL: Restored {container.name}")
            return True
        except:
            return False

    def kill_node(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.kill()
            self.add_log("Admin", f"Manual Termination: {container.name}")
            return True
        except:
            return False
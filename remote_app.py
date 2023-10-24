import time

class App:
    def __init__(self, name, ssh, config=None):
        self.name = name
        self.ssh = ssh
        self.status = {'is_running':False,
                      'last_start_ts':None,
                      'last_kill_ts':None,
                      'last_monitor_ts':None}
        
        self.app_config = {
            'start_app_cmd':'',
            'kill_app_cmd':'',
            'monitor_app_pattern_list':[]}
        
        if config:
            self.app_config = config
        
    def start_app(self):
        try:
            cmd = self.app_config['start_app_cmd']
            self.status['last_start_ts'] = time.time()
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            print(stdout.read(),stderr.read())
        except Exception as e:
            print(f"Error Starting App {self.name} : {e}")
        # if len(stderr.read())>0:
        #     return False
        # else:
        #     return True
            
    def kill_app(self):
        cmd = self.app_config['kill_app_cmd']
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        if len(self.app_config['monitor_app_pattern_list'])>0:
            self.status['last_monitor_ts'] = time.time()
            for k in self.app_config['monitor_app_pattern_list']:
                cmd = f'pkill -9 -f "{k}"'
                stdin, stdout, stderr = self.ssh.exec_command(cmd)

        self.status['last_kill_ts'] = time.time()
        if len(stderr.read())>0:
            return False
        else:
            return True
            
    def monitor_app(self):
        if len(self.app_config['monitor_app_pattern_list'])>0:
            self.status['last_monitor_ts'] = time.time()
            results = []
            for k in self.app_config['monitor_app_pattern_list']:
                cmd = f'ps aux | grep "{k}"'
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                pid_list = self.get_pids_by_pattern(stdout.read().decode())
                results.append(True if len(pid_list)>0 else False)
                
            for r in results:
                if not r:
                    self.status['is_running'] = False
                    return False
            self.status['is_running'] = True
            return True
        else:
            return True

    def get_pids_by_pattern(self, out):
        try:
            result = out
            # Split the result into lines
            lines = result.split('\n')

            # Initialize a list to store matching PIDs
            matching_pids = []

            # Process each line to extract the PID
            for line in lines:
                parts = line.split()
                if len(parts) > 1 and 'grep' not in parts:
                    pid = parts[1]
                    matching_pids.append(pid)
            print(f"Found PIDs: {matching_pids}")
            return matching_pids

        except Exception as e:
            print(f"Error: {e}")
            return []
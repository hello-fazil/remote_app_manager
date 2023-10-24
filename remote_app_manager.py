from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import *
from remote_app import App
import threading
import yaml
import click


class RemoteAppManager:
    def __init__(self):
        # Initialize SSH client
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.sftp = None
        self._log_txt = None
        
        # Define SSH connection parameters
        self.host_config = {'hostname':None,
                            'port':22,
                            'username':None,
                            'password':None,
                            'apps_directory':None}
        
        self.applications_dict = {}

        self.current_app_thread = None
        
    def set_host_config(self, host_config):
        self.print_log(f"HOST CONFIG SET FOR {host_config['username']}@{host_config['hostname']}")
        self.host_config = host_config
    
    def is_host_config_valid(self):
        for k in list(self.host_config.keys()):
            if self.host_config[k] is None:
                return False
        return True
    
    def connect_remote_host(self):
        self.print_log("Attempting to create SSH connection.....")
        if self.is_host_config_valid:
            try:
                self.ssh.connect(self.host_config['hostname'], 
                                self.host_config['port'], 
                                self.host_config['username'], 
                                self.host_config['password'],
                                timeout=5)
                self.sftp = self.ssh.open_sftp()
            except (BadHostKeyException, AuthenticationException, NoValidConnectionsError, SSHException, Exception) as e:
                self.print_log(f"Unable to make connection. Error: {e}",'red')
                return False
            self.print_log('Connection Success!','green')
            return True
        else:
            self.print_log("Host Config Invalid. Unable to make a connection.",'red')
            return False
    
    def populate_applicaltions(self):
        if self.sftp:
            app_files_list = self.sftp.listdir(self.host_config['apps_directory'])
            for app_file in app_files_list:
                try:
                    fn = f"{self.host_config['apps_directory']}/{app_file}"
                    with self.sftp.open(fn, 'r') as file:
                        yaml_data = yaml.safe_load(file)
                        if app_file.split('.')[1]=='yaml':
                            name = app_file.split('.')[0]
                            app = App(name=name,
                                    ssh=self.ssh,
                                    config=yaml_data)
                            self.applications_dict[name] = app
                            print(f"Found App: {name}")
                except Exception as e:
                    print(f"Unable to load app. Error: {e}")
        else:
            print("Unable to populate Apps. sftp not initiated.")
    
    def start_application(self,name):
        if self.current_app_thread:
            self.kill_running_application()
        if not self.current_app_thread:
            if name in self.applications_dict.keys():
                self.print_log(f"Starting App: {name}",'green')
                self.current_app_thread = threading.Thread(target=self.applications_dict[name].start_app(),
                                                           name=name)
                self.current_app_thread.start()
                return True
            else:
                self.print_log('Invalid App Name.','red')
        return False
    
    def kill_running_application(self):
        if self.current_app_thread:
            print(f"Killing Current App: {self.current_app_thread.name}")
            if self.applications_dict[self.current_app_thread.name].kill_app():
                self.current_app_thread.join()
                self.current_app_thread = None
        else:
            self.print_log("No App is running currently")
            return False
    
    def kill_application(self,app_name):
        if app_name in self.applications_dict.keys():
            self.applications_dict[app_name].kill_app()
    
    def get_available_apps(self):
        return list(self.applications_dict.keys())
    
    def is_app_running(self, name):
        try:
            s = self.applications_dict[name].monitor_app()
            return s
        except KeyError:
            self.print_log(f'App: {name} Not Found!','red')
            return False
    
    def is_connected(self):
        try:
            if self.ssh._transport.is_active():
                return True
        except Exception as e:
            self.print_log(f"SSH Client not connected.",'red')
        return False

    def shutdown(self):
        if self.current_app_thread:
            self.kill_running_application()
        self.ssh.close()

    def print_log(self,txt,color=None):
        self._log_txt = txt
        click.secho(txt, fg=color)
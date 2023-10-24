import wx
import time

class DashboardFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(DashboardFrame, self).__init__(*args, **kw)
        self.status = {'current_app':None,
                       'is_connected':False}
        # Creating a main panel
        self.main_panel = wx.Panel(self)
        # self.main_panel.SetBackgroundColour(wx.Colour(253, 241, 245))

        # Create sizers for layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.pane1_sizer = wx.BoxSizer(wx.VERTICAL)
        pane1_1_sizer = wx.BoxSizer(wx.VERTICAL)
        pane1_2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pane1_3_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.pane2_sizer = wx.BoxSizer(wx.VERTICAL)

        # Pane 1: Text entry fields, buttons, and status label
    
        stretch_heading = wx.StaticText(self.main_panel, label="Stretch Connect")
        stretch_heading.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))

        self.username_entry = wx.TextCtrl(self.main_panel, style=wx.TE_PROCESS_ENTER)
        self.username_entry.SetHint('User-Name@Host-name')
        self.password_entry = wx.TextCtrl(self.main_panel, style=wx.TE_PASSWORD)
        self.password_entry.SetHint('Password')
        self.connect_button = wx.Button(self.main_panel, label="Connect")
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect_button_press)
        self.connect_button.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))

        self.disconnect_button = wx.Button(self.main_panel, label="Close")
        self.disconnect_button.SetBackgroundColour(wx.Colour(255,0,0))
        self.disconnect_button.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        self.disconnect_button.Bind(wx.EVT_BUTTON, self.on_connect_button_press)
        self.disconnect_button.Name = 'disconnect_button'
        self.disconnect_button.Hide()

        self.spinner = wx.ActivityIndicator(self.main_panel, size=(30, 30))
        self.spinner.Start()
        # self.spinner.Hide()

        status_label1 = wx.StaticText(self.main_panel, label="Status")
        status_label1.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        self.connection_status_label = wx.StaticText(self.main_panel, label="Disconnected",size=(300, 50))
        self.connection_status_label.SetForegroundColour(wx.Colour(255, 0, 0))
        self.connection_status_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))

        pane1_1_sizer.Add(self.username_entry, 0, wx.EXPAND | wx.ALL, 5)
        pane1_1_sizer.Add(self.password_entry, 0, wx.EXPAND | wx.ALL, 5)

        pane1_2_sizer.Add(self.connect_button, 10, wx.EXPAND | wx.ALL, 5)
        pane1_2_sizer.Add(self.disconnect_button, 10, wx.SHRINK | wx.ALL, 5)

        pane1_3_sizer.Add(status_label1, 0, wx.EXPAND | wx.ALL, 5)
        pane1_3_sizer.Add(self.connection_status_label, 0, wx.EXPAND | wx.ALL, 5)
        pane1_3_sizer.Add(self.spinner, 0, wx.EXPAND | wx.ALL, 5)

        self.pane1_sizer.Add(stretch_heading, 0, wx.EXPAND | wx.ALL, 5)
        self.pane1_sizer.Add(pane1_1_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.pane1_sizer.Add(pane1_2_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.pane1_sizer.Add(pane1_3_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Pane 2: Button and status label, and "Available Apps" section
        available_apps_label = wx.StaticText(self.main_panel, label="Available Apps")
        available_apps_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))

        self.app_status_label = wx.StaticText(self.main_panel, label="Not Connected.",size=(300, 50))
        self.app_status_label.SetForegroundColour(wx.Colour(255, 0, 0))
        self.app_status_label.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.kill_button = wx.Button(self.main_panel, label="Kill")
        self.kill_button.SetForegroundColour(wx.Colour(200, 0, 0))
        self.kill_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        self.kill_button.Bind(wx.EVT_BUTTON, self.on_kill_button_press)
        self.kill_button.Hide()

        self.pane2_sizer.Add(self.kill_button, 0, wx.CENTER | wx.ALL, 5)
        self.pane2_sizer.Add(available_apps_label, 0, wx.EXPAND | wx.ALL, 5)
        self.pane2_sizer.Add(self.app_status_label, 0, wx.EXPAND | wx.ALL, 5)
        
              
        # Add pane sizers to main sizer
        self.main_sizer.Add(self.pane1_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.pane2_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.main_panel.SetSizer(self.main_sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        # Fit the window to the content
        self.main_sizer.Fit(self)
    
    def update(self,event):
        if self.status['is_connected']:
            if self.status['current_app']:
                for b in self.app_buttons_list:
                    if b.Name==self.status['current_app']:
                        name_label = b.GetLabelText() 
                        self.kill_button.SetLabelText(f"Kill {name_label}")
                        self.app_status_label.SetLabel(f"Rnning {name_label}")
                        b.SetBackgroundColour(wx.Colour(0, 128, 0))
                    else:
                        b.Disable()
                self.kill_button.Show()
                self.app_status_label.SetForegroundColour(wx.Colour(0, 255, 0))
            else:
                self.app_status_label.SetLabel("No App Running Currently.")
                self.app_status_label.SetForegroundColour(wx.Colour(255, 0, 0))
                for b in self.app_buttons_list:
                    b.Enable()
                    b.SetBackgroundColour(wx.Colour(100, 100, 100))
        else:
            self.app_status_label.SetLabel("Not Connected.")
            self.app_status_label.SetForegroundColour(wx.Colour(255, 0, 0))
            self.kill_button.Hide()
        self.main_sizer.Fit(self)
    
    def on_kill_button_press(self, event):
        self.status['current_app'] = None
        self.kill_button.Hide()
    
    def on_connect_button_press(self,event):
        o = event.GetEventObject()
        if o.Name!='disconnect_button':
            self.status['is_connected'] = True
            self.connect_button.SetBackgroundColour(wx.Colour(0, 128, 0))
            self.connect_button.SetLabelText("Connected")
            self.connection_status_label.SetLabelText("Connection Success!")
            self.connection_status_label.SetForegroundColour(wx.Colour(0, 128, 0))
            self.disconnect_button.Show()
            self.populate_apps()
        else:
            self.status['is_connected'] = False
            self.connect_button.SetBackgroundColour(wx.Colour(0, 128, 0))
            self.connect_button.SetLabelText("Connect")
            self.connection_status_label.SetLabelText("Not Connected!")
            self.connection_status_label.SetForegroundColour(wx.Colour(255, 0, 0))
            self.disconnect_button.Hide()
            for b in self.app_buttons_list:
                b.Hide()
            self.app_buttons_list = None
        self.main_sizer.Fit(self)

    
    def on_app_button_press(self,event):
        self.status['current_app'] = event.GetEventObject().Name

    def populate_apps(self):
        button3 = wx.Button(self.main_panel, label="Gamepad", style=wx.BU_EXACTFIT)
        button3.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        
        button4 = wx.Button(self.main_panel, label="Stretch Web Interface", style=wx.BU_EXACTFIT)
        button4.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        
        button5 = wx.Button(self.main_panel, label="HomeRobot OVMM", style=wx.BU_EXACTFIT)
        button5.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))

        button3.Name = 'gamepad'
        button4.Name = 'web_interface'
        button5.Name = 'homerobot'

        self.app_buttons_list = [button3,
                                 button4,
                                 button5]
        
        button3.Bind(wx.EVT_BUTTON, self.on_app_button_press)
        button4.Bind(wx.EVT_BUTTON, self.on_app_button_press)
        button5.Bind(wx.EVT_BUTTON, self.on_app_button_press)

        self.pane2_sizer.Add(button3, 0, wx.EXPAND | wx.ALL, 5)
        self.pane2_sizer.Add(button4, 0, wx.EXPAND | wx.ALL, 5)
        self.pane2_sizer.Add(button5, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Fit(self)
        self.timer.Start(500)

if __name__ == '__main__':
    app = wx.App(False,useBestVisual=True)
    frame = DashboardFrame(None, wx.ID_ANY, "Remote Dashboard")
    frame.Show()
    app.MainLoop()

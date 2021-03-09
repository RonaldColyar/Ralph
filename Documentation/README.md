<h1 align = "center"  > <img  width = "300px" src = "https://github.com/RonaldColyar/Ralph/blob/main/Documentation/Ralph.png" /> </h1>
<h1 align = "center"> Welcome To Ralph's Documentation!</h1>
<h2 align = "center"> Making Home Security Fun!! 🏎️ </h2>


### How is the RC car controlled❓
<p> The RC car is controlled using the Raspberry Pi <a href = "https://github.com/RonaldColyar/Ralph/tree/main/DemonSlayerCorps" >Client <a/> that manipulates the 
  GPIO! The GPIO and the RC car circuits are directly connected via wire! </p>

### Why use a proxy server❓
<p> The Desktop/Raspberry Pi client should be able to 
  relocate to different addresses. Making them bound to a certain network(and connecting over that network )
  would limit the mobility of this system! 
</p>


### Disclaimer

<p> The documentation is here to give you a run through of the data flow. The code in the documentation will change over time. I will try my best to keep the documentation updated!</p>




# Proxy Server( [GiyuTomioka](https://github.com/RonaldColyar/Ralph/tree/main/GiyuTomioka)):
### The proxy server is wrapped in the class `Interface`
### The starting point of the proxy server is ` start_server(self)`
  ```python 
      def start_server(self):
        while self.running == True  and self.connected<2:
            client , addr = self.server.accept()
            self.connected += 1 
            thread = threading.Thread(target = self.check_declaration , args=(client,addr) )
            thread.start()
  
 ```
 
 <p>A new thread is started for every new connection(Maximum of two for now) to avoid blocking other connections</p>

### Incoming connections are controlled by `check_declaration(self,client,addr)` 
```python
   def check_declaration(self,client,addr):

        connector_number = self.number_of_new_connector() #for clock purposes
        self.time_tracker.start_timer(client,connector_number) #prevent blocking!
        try:
            client.send("WHO_ARE_YOU".encode("ascii"))
            declaration = client.recv(100).decode("ascii")
            self.time_tracker.stop_timer(connector_number)
            self.check_declaration_tier_two(declaration,addr,client)
        except Exception as e:
            print("Issue")

```
<p> check_declaration pings the Client for information about who they are!
  The client could either be the <a href = "https://github.com/RonaldColyar/Ralph/tree/main/DemonSlayerCorps" >Raspberry Pi <a/> or <a href = "https://github.com/RonaldColyar/Ralph/tree/main/TanjiroKamado" >The desktop client. <a/>  
  </p>  
  
 ### Since   `declaration = client.recv(100).decode("ascii")` blocks the thread  
 
 <p> there is a <a href = "https://github.com/RonaldColyar/Ralph/blob/main/GiyuTomioka/TimeoutManager.py"> time out manager </a> that checks to see if a client has been connected for more than 20 seconds(without stating who they are) before timing them out!: </p> 
 
 ### By calling  `start_timer(self , client,num)`the 20 second  countdown begins! 
 
 ```python
 
      def start_timer(self , client,num):
        thread = threading.Thread(target = self.monitor_timeout , args = (client,num))
        thread.start()
 ```
 ### Once the client responds with who they are `stop_timer(self ,num)` is called and we proceed to check the actual declaration with  `check_declaration_tier_two(self,declaration,addr,client)`:
 
 
 ```python
     def check_declaration_tier_two(self,declaration,addr,client):
        if declaration == "DESKTOP" and self.desktop_client == None :
                self.desktop_client == client 
                self.successful_event(self.desktop_client ,
                            client,self.pi_client,"AWAITING_PI") 
        elif declaration == "DESKTOP" and self.desktop_client != None:
                self.failed_event(client , "ALREADYDESKTOP",addr)

        else:
                self.check_declaration_tier_three(declaration,client,addr)
 
 ```
 
 ### Separating the declaration checks into smaller methods for best practice, here is tier three :
 
 ```python
     def check_declaration_tier_three(self,declaration,client,addr):
        if declaration == "PI" and self.pi_client == None:
            self.successful_event(self.pi_client,
                    client,self.desktop_client,"AWAITING_DE") 
        elif declaration == "PI" and self.pi_client != None:
            self.failed_event(client ,"ALREADYPI",addr)
        elif declaration == None:
            return
        else:
            print("Unknown Command!")
            failed_event(client , "Unknown Command!",addr)
 
 
 ```
  <p>Here we check for  conflicting declarations. For example , if one client claims that they're the desktop client but there is already a claimed desktop client connected we have a conflict of declaration because there can only be one desktop/pi. Once this conflict is discovered we trigger the failed event: </p>
  

 
 
 ```python
   def failed_event(client,message,addr):
        self.connected -= 1
        client.send(message)
        client.close()
        if message == "ALREADYPI":
            self.logger.conflicting_declaration("PI" , addr)
        else:
            self.logger.conflicting_declaration("Desktop" ,addr)
        self.logger.disconnection(addr)

 
 ```
 
 
 
 ### If there is no failed event the ` successful_event(self,class_client_ref,client,other_client,message)` is triggered: 

 
 ```python
     def successful_event(self,class_client_ref,client
                        ,other_client,message):

            class_client_ref = client
            if other_client != None: 
                client.send("SUCCESS".encode("ascii"))
                other_client.send("SUCCESS".encode("ascii"))
                thread = threading.Thread(target =self.video_thread)
                thread.start()
                self.listen_for_movement()
            else:
                client.send(message.encode("ascii"))
 ```
 
  ### Parameters:
  
  -  `class_client_ref` refers to  the  `self.pi_client`/`self.desktop_client ` states held by the `Interface Class`
  - `other_client` refers to the opposing client state. For example one connection claims to be "DESKTOP" the `other_client `would be  `self.pi_client` and the  `class_client_ref` would be `self.desktop_client` 
  - `client` refers to the connection(socket object) object passed from the original acception of connection in `start_server(self)`
  -  `message` updates the `client` on the status of the `other_client` if the `other_client` isn't connected! 
  
  
  ### when the successful event is triggered:
 
  - the   `video_thread` is started(this thread streams video from the pi to the desktop).
  - the  main thread is then blocked by  `listen_for_movement` which sends movement commands from the desktop to the pi.
 <hr>

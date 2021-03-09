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
 
 ### by calling  `start_timer(self , client,num)`the 20 second  countdown begins! 
 
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
  <p>Here we check for  conflicting declarations. For example , if one client claims that they're the desktop client but there is already a claimed desktop client connected we have a conflict of declaration because there can only be one desktop/pi. </p>
  
 
  
 <hr>

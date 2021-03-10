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
 
 
# Raspberry Pi Client( [DemonSlayerCorps](https://github.com/RonaldColyar/Ralph/tree/main/DemonSlayerCorps)):
### The start of the pi client is `start_client(self)`:
```python 

	def start_client(self):
		self.running = True
		who_response = self.client.recv(100).decode("ascii")
		if who_response == "WHO_ARE_YOU":
			client.send("PI".encode("ascii"))
			server_response = self.client.recv(100).decode("ascii")
			self.check_response_and_proceed(server_response)

```

<p> First we wait on a response from the server that should question who we claim to be(Desktop or Pi). </p>


- We declate that we are the PI.
- We then check the response to the declaration with  `check_response_and_proceed(self ,response)`:


```python

	def check_response_and_proceed(self ,response):
			if response == "SUCCESS":
				print(colored("Successfully paired! Starting Client....","green"))
				self.start_threads()
			elif response == "AWAITING_DE":
				print(colored("Server says-> Waiting on desktop!" , "green"))
				self.wait_for_desktop()
			elif response == "ALREADYPI":
				print("Server says->"+
					colored("There is already a PI connected!", "red"))
			else:
				print("Server says->" ,
					colored("you have sent an unknown command!" , "red"))

```

<p>If we get a "SUCCESS" message then we know there is a desktop client connected !  </p>


### We can now begin to stream data/listen for movements with `start_threads(self)`:

  ```python
  	def start_threads(self):
		movement_thread = threading.Thread(target = self.listen_for_messages)
		streaming_thread = threading.Thread(target = self.stream_video)
		movement_thread.start()
		streaming_thread.start()
   ```



###  What happens if the desktop connects? There will be lingering threads streaming to the proxy for no reason!

### We handle this issue in `listen_for_messages(self)`:


```python
	def listen_for_messages(self):
		while self.running == True:
			message = self.client.recv(100).decode("ascii")
			decrypted_message = eh.decrypted(message)
			if decrypted_message == '-DesktopDisconnect':
				thread = threading.Thread(target = self.stop_streaming_and_wait_for_desktop)
				thread.start()
				break #stop listening for messages(end current thread)
			
			else:
				self.route_movement(decrypted_message)

```

<p>Note: There will only be two types of messages that reach the pi : Movements and Declarations of disconnecting </p>


<p> In the above block(one of the two threads running on the pi) we decrypt each message and check if the message was a declaration that the desktop disconnected! </p>

<p> If there was a disconnect declaration we start a new thread that stops the streaming thread and begin to wait for the desktop to connect again!   </p>
### that thread started by the function call `stop_streaming_and_wait_for_desktop(self)` from  `thread = threading.Thread(target = self.stop_streaming_and_wait_for_desktop)`



###Instead of letting the thread loop around again we just `break` from the `listen_for_messages` thread  after starting this new thread!

### how is the  streaming thread stopped?:

```python 
	def stop_streaming_and_wait_for_desktop(self):
			self.running = False#stop  the video streaming thread!
			time.sleep(8)  #give enough time to close
			self.running = True
			self.wait_for_desktop()

```
###   `self.running `  controls the while condition of the streaming thread. Setting it to false and waiting 8 seconds give the thread enough time to stop.

### Now we `self.wait_for_desktop()`:


```python
	def wait_for_desktop(self):
		server_response = self.client.recv(100).decode("ascii")
		if server_response == "SUCCESS":
			self.start_threads()
		else:
			self.client.close()
			print("issue!!")

```

<p>We wait untill the desktop is connected and then we start up the threads again. </p>

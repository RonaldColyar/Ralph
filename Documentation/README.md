<h1 align = "center"  > <img  width = "300px" src = "https://github.com/RonaldColyar/Ralph/blob/main/Documentation/Ralph.png" /> </h1>
<h1 align = "center"> Welcome To Ralph's Documentation!</h1>
<h2 align = "center"> Making Home Security Fun!! 🏎️ </h2>


## How is the RC car controlled❓
<p> The RC car is controlled using the Raspberry Pi <a href = "https://github.com/RonaldColyar/Ralph/tree/main/DemonSlayerCorps" >Client <a/> that manipulates the 
  GPIO! The GPIO and the RC car circuits are directly connected via wire! </p>

## Why use a proxy server❓
<p> The Desktop/Raspberry Pi client should be able to 
  relocate to different addresses. Making them bound to a certain network(and connecting over that network )
  would limit the mobility of this system! 
</p>

<hr>

# Actual Documentation

<p>Disclaimer - The documentation is here to give you a run through of the data flow. The code in the documentation will change over time. I will try my best to keep the documentation updated!</p>




### Proxy Server( [GiyuTomioka](https://github.com/RonaldColyar/Ralph/tree/main/GiyuTomioka)):

#### Incoming connections are controlled by `check_declaration(self,client,addr)` 
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
  The client could either be the <a href = "https://github.com/RonaldColyar/Ralph/tree/main/DemonSlayerCorps" >Raspberry Pi <a/> or <a href = "https://github.com/RonaldColyar/Ralph/tree/main/TanjiroKamado" >The desktop client <a/>  
  </p>

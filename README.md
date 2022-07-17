# SBC - Messages App 
The Final Project in Computer Networking Course , Ariel University's C.S Faculty. <br/>
There goal here is to create a multi client chat app (that we called SBC), That will allow the clients to speak to each other as well as download some file (`txt` / `png` / `mp3` and more) from the server.</br>
But, for the sake of practice, We were required to meet the following tasks:
 - To Create a GUI for the Server and for the Clients.
 - To create a private chat and also a public chat option (with all users).
 - To implement the chat using TCP Soket, and create commend words that the Client will type and send, then no other Client will see that,  but the Server will send back the requested commend (such as `<users_get>` , `<all_msg_set>`, `<name_file><download>` ).
 - To implement download of files using Reliable UDP Soket.

</br>

that means that every client will have two separate Soket connections, first is TCP soket for chating and the second is reliable UDP soket for receiving files from the Server.</br> The reliable UDP soket is achived by Implementing RDT over UDP with Congestion control and Sliding Window Protocol. 

# How to run
### First :
Open the GUI folder from terminal.
### Second : 
To open server type in the command: `python3 ServerGUI.py` </br>
To open the client and connect type the command: `python3 SBChatApp.py`



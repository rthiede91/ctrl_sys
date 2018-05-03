/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;

import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import user.control.login;

/**
 *
 * @author Thiedes
 */
public class connection implements Runnable 
{
	private String host;
	private int port;

	public connection(String host, int port)
        {
		this.host = host;
		this.port = port;
	}

	public void run()
        {
            try(Socket server = new Socket(this.host, this.port); 
                Scanner cmd = new Scanner(System.in); 
                PrintStream sendMsg = new PrintStream(server.getOutputStream())) 
            {
                readConnection r = new readConnection(server);
                new Thread(r).start();
                
                while (cmd.hasNextLine()) 
                {
                    sendMsg.write(cmd.nextLine().getBytes());
                }
                

            } 
            catch (IOException ex) 
            {
                Logger.getLogger(connection.class.getName()).log(Level.SEVERE, null, ex);
            }
	}
}
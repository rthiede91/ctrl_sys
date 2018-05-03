/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;

import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Thiedes
 */

public class functions implements Runnable 
{
    private String cmd;
    private Socket server;
    
    public functions(String cmd, Socket server ) 
    {
        this.cmd = cmd;
        this.server = server;
    }

    public void run() 
    {
        try 
        {
            PrintStream sendMsg = new PrintStream(this.server.getOutputStream());
            
            if (this.cmd.equals("check"))
            {
                System.err.println("Done!!!");
                Thread.sleep(1000);
                this.server.close();
            }
            
            if (this.cmd.equals("identify"))
            {
                System.err.println("send");
                Thread.sleep(2000);
                sendMsg.write("identify;user".getBytes());
            }
        }
        catch (InterruptedException ex)
        {
            Logger.getLogger(functions.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) 
        {
            Logger.getLogger(functions.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }

}

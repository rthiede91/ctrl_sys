/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 *
 * @author Thiedes
 */
public class readConnection implements Runnable 
{
    private Socket server;

    public readConnection(Socket server) 
    {
            this.server = server;
    }

    public void run() 
    {
        try 
        {
            BufferedReader buf =
            new BufferedReader(new InputStreamReader(this.server.getInputStream()));
            
            String read = "";
            
            while((read = buf.readLine()) != null)
            {
                if (read.equals("eventStart"))
                {
                    String blob;
                    String blobImage = "";
                    while(!(blob = buf.readLine()).equals("endImage"))
                    {
                        blobImage += blob;
                    }
                    String info = buf.readLine();
                    read += ";"+blobImage+";"+info;
                }
                
                functions func = new functions(read,server);
                new Thread(func).start();
            }
        }
        catch (IOException ex) 
        {
            Logger.getLogger(readConnection.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
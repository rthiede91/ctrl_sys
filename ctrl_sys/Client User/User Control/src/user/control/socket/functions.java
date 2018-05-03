/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.util.Base64;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import user.control.viewer;

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
            //System.out.println(cmd);
            
            if (this.cmd.equals("check"))
            {
                /*ResultSet rs = stmt.executeQuery(<Your Query SQL>);  
                java.sql.Blob blob = rs.getBlob(column);  
                InputStream in = blob.getBinaryStream();  
                BufferedImage image = ImageIO.read(in);*/
                
                
                viewer vw = new viewer();
                    vw.show();
                    
            }
            
            if (cmd.contains(";"))
            {
               
                String [] data = cmd.split(";");
                
                
                System.out.println(cmd);

                Scanner s=new Scanner(System.in);  
                
                //System.out.println("Enter base64 string to be converted to image"); 
                
                //String base64=s.nextLine();  
                String base64=data[1];
                
                byte[] base64Val=Base64.getDecoder().decode(base64);                
                
                File imgFile = new File("./pic.png");  
                BufferedImage img = ImageIO.read(new ByteArrayInputStream(base64Val));  
                ImageIO.write(img, "png", imgFile);
                
                sendMsg.write("ok".getBytes());
            
            }
            if (this.cmd.equals("identify"))
            {
                sendMsg.write("identify;user".getBytes());
            }
               
        } 
        catch (IOException ex) 
        {
            Logger.getLogger(functions.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }

}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control;

import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
import user.control.socket.connection;
import user.control.socket.functions;

/**
 *
 * @author Thiedes
 */
public class UserControl 
{
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws InterruptedException 
    {
        for (int a=0;a<=100;a++)
        {
            System.out.println("tn: "+a);
            Thread.sleep(100);
            connection  conn = new connection("187.11.123.175", 8081);
            new Thread(conn).start();
        }
        

        //new connection("187.11.123.175", 8081).run();
    }
    
}

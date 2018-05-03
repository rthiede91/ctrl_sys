/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control;

import user.control.socket.connection;

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
 
        Thread.sleep(100);
        connection  conn = new connection("10.0.1.229", 8081);
        new Thread(conn).start();
        
        //new connection("187.11.123.175", 8081).run();
    }
    
}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;
import java.io.InputStream;
import java.util.Scanner;
/**
 *
 * @author Thiedes
 */
public class readConnection implements Runnable 
{
    private InputStream servidor;

    public readConnection(InputStream servidor) 
    {
            this.servidor = servidor;
    }

    public void run() 
    {
            try(Scanner s = new Scanner(this.servidor))
            {
                    while (s.hasNextLine()) 
                    {
                            System.out.println(s.nextLine());
                    }
            }
    }
}
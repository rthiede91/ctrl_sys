/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package user.control.socket;

import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

/**
 *
 * @author Thiedes
 */
public class connection 
{
	private String host;
	private int porta;

	public connection(String host, int porta)
        {
		this.host = host;
		this.porta = porta;
	}

	public void run() throws UnknownHostException, IOException 
        {
		try(Socket cliente = new Socket(this.host, this.porta); 
				Scanner teclado = new Scanner(System.in); 
				PrintStream saida = new PrintStream(cliente.getOutputStream())) 
                {
		
                    readConnection r = new readConnection(cliente.getInputStream());
                    new Thread(r).start();

                    while (teclado.hasNextLine()) 
                    {
                            saida.println(teclado.nextLine());
                    }
		}
	}
}
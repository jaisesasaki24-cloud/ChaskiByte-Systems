package pe.edu.upeu.cliente.controller;

import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.cliente.entity.Cliente;
import java.util.List;
import java.util.Arrays;

@RestController
@RequestMapping("/api/v1/clientes")
public class ClienteController {

    @GetMapping
    public List<Cliente> listarClientes() {
        return Arrays.asList(
            new Cliente("Eliceo Parillo Mostajo", "eliceo@chaskipc.pe", "70889911"),
            new Cliente("Cristhian Paul Laura Vargas", "cristhian@chaskipc.pe", "72445566")
        );
    }

    @GetMapping("/health-check")
    public String health() {
        return "PAGATU-CLIENTE-MS activo y registrado en Eureka";
    }
}

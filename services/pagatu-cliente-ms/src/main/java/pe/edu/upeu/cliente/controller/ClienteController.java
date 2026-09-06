package pe.edu.upeu.cliente.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.cliente.entity.Cliente;

import java.util.*;

@RestController
@RequestMapping("/api/v1/clientes")
public class ClienteController {

    private final List<Cliente> clientesDb = new ArrayList<>();

    public ClienteController() {
        // Datos semilla iniciales
        Cliente c1 = new Cliente("DNI", "70889911", "Eliceo", "Parillo Mostajo", 
                                 null, "Av. Circunvalacion 450, Juliaca", "eliceo@chaskipc.pe", "951234567");
        c1.setId(1L);

        Cliente c2 = new Cliente("DNI", "72445566", "Cristhian Paul", "Laura Vargas", 
                                 null, "Jr. Huancane 230, Juliaca", "cristhian@chaskipc.pe", "952345678");
        c2.setId(2L);

        Cliente c3 = new Cliente("RUC", "20601234567", null, null, 
                                 "CHASKIBYTE SYSTEMS S.A.C.", "Av. Manuel Nuñez Butron 120, Puno", "contacto@chaskibyte.com", "051328900");
        c3.setId(3L);

        clientesDb.add(c1);
        clientesDb.add(c2);
        clientesDb.add(c3);
    }

    @GetMapping
    public List<Cliente> listarClientes() {
        return clientesDb;
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> obtenerPorId(@PathVariable Long id) {
        return clientesDb.stream()
                .filter(c -> c.getId().equals(id))
                .findFirst()
                .<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("error", "Cliente no encontrado", "id", id)));
    }

    @PostMapping
    public ResponseEntity<?> registrarCliente(@RequestBody Cliente nuevoCliente) {
        if (nuevoCliente.getNumeroDocumento() == null || nuevoCliente.getNumeroDocumento().trim().isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "El número de documento es obligatorio."));
        }
        nuevoCliente.setId((long) (clientesDb.size() + 1));
        clientesDb.add(nuevoCliente);
        return ResponseEntity.status(HttpStatus.CREATED).body(nuevoCliente);
    }

    /**
     * Consulta y Autocompletado simulado de RENIEC (DNI de 8 dígitos)
     * Utilizado en S2 para registro y verificación de identidad de clientes
     */
    @GetMapping("/consulta-reniec/{dni}")
    public ResponseEntity<?> consultarReniec(@PathVariable String dni) {
        if (dni == null || !dni.matches("\\d{8}")) {
            return ResponseEntity.badRequest().body(Map.of(
                "error", "El DNI ingresado debe contener exactamente 8 dígitos numéricos.",
                "dni_invalido", dni
            ));
        }

        // Mock oficial de consulta RENIEC
        Map<String, Object> reniecData = new LinkedHashMap<>();
        reniecData.put("fuente", "RENIEC - Registro Nacional de Identificación y Estado Civil");
        reniecData.put("dni", dni);
        reniecData.put("nombres", dni.equals("70889911") ? "Eliceo" : "Juan Carlos");
        reniecData.put("apellidoPaterno", dni.equals("70889911") ? "Parillo" : "Mamani");
        reniecData.put("apellidoMaterno", dni.equals("70889911") ? "Mostajo" : "Quispe");
        reniecData.put("nombreCompleto", dni.equals("70889911") ? "Eliceo Parillo Mostajo" : "Juan Carlos Mamani Quispe");
        reniecData.put("digitoVerificador", String.valueOf((dni.charAt(7) - '0' + 3) % 10));
        reniecData.put("estadoDni", "VIGENTE");
        reniecData.put("codigoUbigeo", "211101");
        reniecData.put("departamento", "PUNO");
        reniecData.put("provincia", "SAN ROMAN");
        reniecData.put("distrito", "JULIACA");

        return ResponseEntity.ok(reniecData);
    }

    /**
     * Consulta y Validación Tributaria simulada de SUNAT (RUC de 11 dígitos)
     * Utilizado en S2 para emisión de Facturas y verificación de contribuyentes
     */
    @GetMapping("/consulta-sunat/{ruc}")
    public ResponseEntity<?> consultarSunat(@PathVariable String ruc) {
        if (ruc == null || !ruc.matches("\\d{11}")) {
            return ResponseEntity.badRequest().body(Map.of(
                "error", "El RUC ingresado debe contener exactamente 11 dígitos numéricos.",
                "ruc_invalido", ruc
            ));
        }

        boolean esEmpresa = ruc.startsWith("20");
        Map<String, Object> sunatData = new LinkedHashMap<>();
        sunatData.put("fuente", "SUNAT - Superintendencia Nacional de Aduanas y de Administración Tributaria");
        sunatData.put("ruc", ruc);
        sunatData.put("razonSocial", esEmpresa ? "CHASKIBYTE SYSTEMS S.A.C." : "PARILLO MOSTAJO ELICEO");
        sunatData.put("estadoContribuyente", "ACTIVO");
        sunatData.put("condicionDomicilio", "HABIDO");
        sunatData.put("tipoContribuyente", esEmpresa ? "SOCIEDAD ANONIMA CERRADA" : "PERSONA NATURAL CON NEGOCIO");
        sunatData.put("direccionFiscal", esEmpresa ? "AV. MANUEL NUÑEZ BUTRON 120 - PUNO" : "AV. CIRCUNVALACION 450 - JULIACA");
        sunatData.put("emisionElectronica", List.of("FACTURA ELECTRONICA", "BOLETA DE VENTA ELECTRONICA"));
        sunatData.put("afectoIGV", true);

        return ResponseEntity.ok(sunatData);
    }

    @GetMapping("/health-check")
    public ResponseEntity<?> health() {
        return ResponseEntity.ok(Map.of(
            "status", "UP",
            "service", "PAGATU-CLIENTE-MS",
            "puerto", 8084,
            "modulos", List.of("Perfil de Cliente", "Validador RENIEC DNI", "Validador SUNAT RUC")
        ));
    }
}

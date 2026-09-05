package pe.edu.upeu.orden.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import pe.edu.upeu.orden.entity.DetalleOrden;
import pe.edu.upeu.orden.entity.Orden;
import pe.edu.upeu.orden.repository.OrdenRepository;

import java.math.BigDecimal;
import java.util.ArrayList;

/**
 * Semilla de datos automática para Órdenes ChaskiPC.
 * Si la base de datos está vacía en cualquier computadora (como la de laboratorio),
 * inserta automáticamente órdenes de prueba completas con ítems de hardware e IGV.
 */
@Component
public class OrdenDataInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(OrdenDataInitializer.class);

    private final OrdenRepository ordenRepository;
    private final OrdenService ordenService;

    public OrdenDataInitializer(OrdenRepository ordenRepository, OrdenService ordenService) {
        this.ordenRepository = ordenRepository;
        this.ordenService = ordenService;
    }

    @Override
    public void run(String... args) {
        if (ordenRepository.count() == 0) {
            log.info("[CHASKIPC-ORDEN] Base de datos vacia. Precargando ordenes de prueba iniciales...");

            // Orden 1: Boleta Simple de Hardware Gamer
            Orden o1 = new Orden();
            o1.setCliente("Eliceo Parillo Mostajo");
            o1.setClienteId(101L);
            o1.setCodigoOrden("ORD-CHK-001");
            o1.setTipoComprobante("BOLETA_SIMPLE");
            o1.setMetodoPago("MERCADO_PAGO");
            o1.setEstado("PAGADO");
            o1.setDetalles(new ArrayList<>());

            DetalleOrden d1 = DetalleOrden.builder()
                    .productoId(1L)
                    .nombreProducto("AMD Ryzen 7 7800X3D (8C/16T)")
                    .precioUnitario(new BigDecimal("1780.00"))
                    .cantidad(1)
                    .build();

            DetalleOrden d2 = DetalleOrden.builder()
                    .productoId(4L)
                    .nombreProducto("Kingston Fury Renegade 1TB NVMe Gen4")
                    .precioUnitario(new BigDecimal("380.00"))
                    .cantidad(1)
                    .build();

            o1.agregarDetalle(d1);
            o1.agregarDetalle(d2);
            ordenService.guardar(o1);

            // Orden 2: Factura para Workstation de Computo
            Orden o2 = new Orden();
            o2.setCliente("ChaskiByte Systems EIRL");
            o2.setClienteId(102L);
            o2.setCodigoOrden("ORD-CHK-002");
            o2.setTipoComprobante("FACTURA");
            o2.setMetodoPago("TRANSFERENCIA");
            o2.setEstado("PENDIENTE");
            o2.setDetalles(new ArrayList<>());

            DetalleOrden d3 = DetalleOrden.builder()
                    .productoId(2L)
                    .nombreProducto("NVIDIA GeForce RTX 4070 SUPER 12GB")
                    .precioUnitario(new BigDecimal("2890.00"))
                    .cantidad(1)
                    .build();

            DetalleOrden d4 = DetalleOrden.builder()
                    .productoId(3L)
                    .nombreProducto("Corsair Vengeance RGB 32GB (2x16GB) DDR5")
                    .precioUnitario(new BigDecimal("520.00"))
                    .cantidad(2)
                    .build();

            o2.agregarDetalle(d3);
            o2.agregarDetalle(d4);
            ordenService.guardar(o2);

            log.info("[CHASKIPC-ORDEN] 2 ordenes de prueba precargadas con exito (Total registros: {})", ordenRepository.count());
        } else {
            log.info("[CHASKIPC-ORDEN] La base de datos ya contiene {} ordenes registradas. Omitiendo precarga.", ordenRepository.count());
        }
    }
}

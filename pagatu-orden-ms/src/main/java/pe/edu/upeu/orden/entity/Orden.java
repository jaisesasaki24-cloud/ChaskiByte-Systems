package pe.edu.upeu.orden.entity;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "ordenes")
public class Orden {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 50)
    private String codigoOrden;

    @Column(nullable = false, length = 150)
    private String cliente;

    private Long clienteId;

    @Builder.Default
    private LocalDateTime fechaCreacion = LocalDateTime.now();

    @Column(precision = 10, scale = 2)
    private BigDecimal subtotal;

    @Column(precision = 10, scale = 2)
    private BigDecimal igv;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal total;

    @Builder.Default
    @Column(length = 30)
    private String estado = "PENDIENTE"; // PENDIENTE, PAGADO, CANCELADO, ENVIADO

    @Builder.Default
    @Column(length = 30)
    private String tipoComprobante = "BOLETA_SIMPLE"; // BOLETA_SIMPLE, BOLETA_CON_DNI, FACTURA

    @Builder.Default
    @Column(length = 30)
    private String metodoPago = "TARJETA"; // TARJETA, YAPE_PLIN, EFECTIVO

    @OneToMany(mappedBy = "orden", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference
    @Builder.Default
    private List<DetalleOrden> detalles = new ArrayList<>();

    public void agregarDetalle(DetalleOrden detalle) {
        detalles.add(detalle);
        detalle.setOrden(this);
    }
}

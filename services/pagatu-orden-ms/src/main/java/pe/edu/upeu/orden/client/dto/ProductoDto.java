package pe.edu.upeu.orden.client.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductoDto {
    private Long id;
    private String sku;
    private String nombre;
    private String marca;
    private BigDecimal precio;
    private Integer stockDisponible;
    private Long categoriaId;
    private String imagenUrl;
}

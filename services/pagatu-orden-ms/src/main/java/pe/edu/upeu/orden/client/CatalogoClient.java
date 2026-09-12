package pe.edu.upeu.orden.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;
import pe.edu.upeu.orden.client.dto.ProductoDto;

@FeignClient(name = "pagatu-catalogo-ms")
public interface CatalogoClient {

    @GetMapping("/api/v1/productos/{id}")
    ProductoDto obtenerProductoPorId(@PathVariable("id") Long id);

    @PutMapping("/api/v1/productos/{id}/stock")
    ProductoDto actualizarStock(@PathVariable("id") Long id, @RequestParam("cantidad") int cantidad);
}

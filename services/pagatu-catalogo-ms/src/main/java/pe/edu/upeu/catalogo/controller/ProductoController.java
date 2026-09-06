package pe.edu.upeu.catalogo.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.catalogo.entity.Producto;
import pe.edu.upeu.catalogo.service.CatalogoService;
import java.util.List;

@RestController
@RequestMapping("/api/v1/productos")
public class ProductoController {

    private final CatalogoService service;

    public ProductoController(CatalogoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Producto> listar(@RequestParam(required = false) Long categoriaId) {
        if (categoriaId != null) {
            return service.buscarPorCategoria(categoriaId);
        }
        return service.listarProductos();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Producto> buscarPorId(@PathVariable Long id) {
        return service.buscarProductoPorId(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/sku/{sku}")
    public ResponseEntity<Producto> buscarPorSku(@PathVariable String sku) {
        return service.buscarPorSku(sku)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Producto> crear(@RequestBody Producto producto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.guardarProducto(producto));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Producto> actualizar(@PathVariable Long id, @RequestBody Producto producto) {
        return service.buscarProductoPorId(id)
            .map(p -> {
                producto.setId(id);
                return ResponseEntity.ok(service.guardarProducto(producto));
            })
            .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}/stock")
    public ResponseEntity<Producto> actualizarStock(@PathVariable Long id, @RequestParam int cantidad) {
        try {
            return ResponseEntity.ok(service.actualizarStock(id, cantidad));
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        service.eliminarProducto(id);
        return ResponseEntity.noContent().build();
    }
}

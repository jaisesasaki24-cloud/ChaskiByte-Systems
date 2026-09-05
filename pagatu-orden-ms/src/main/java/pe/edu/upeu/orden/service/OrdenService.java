package pe.edu.upeu.orden.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pe.edu.upeu.orden.entity.DetalleOrden;
import pe.edu.upeu.orden.entity.Orden;
import pe.edu.upeu.orden.repository.OrdenRepository;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class OrdenService {
    private final OrdenRepository repository;

    public OrdenService(OrdenRepository repository) {
        this.repository = repository;
    }

    public List<Orden> listar() {
        return repository.findAll();
    }

    public Optional<Orden> buscarPorId(Long id) {
        return repository.findById(id);
    }

    @Transactional
    public Orden guardar(Orden orden) {
        if (orden.getFechaCreacion() == null) {
            orden.setFechaCreacion(LocalDateTime.now());
        }
        if (orden.getCodigoOrden() == null || orden.getCodigoOrden().isBlank()) {
            orden.setCodigoOrden("ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase());
        }

        // Si contiene detalles, calcular subtotales y 18% de IGV
        if (orden.getDetalles() != null && !orden.getDetalles().isEmpty()) {
            BigDecimal subtotalCalculado = BigDecimal.ZERO;
            for (DetalleOrden d : orden.getDetalles()) {
                d.setOrden(orden);
                if (d.getPrecioUnitario() != null && d.getCantidad() != null) {
                    BigDecimal itemSub = d.getPrecioUnitario().multiply(new BigDecimal(d.getCantidad()));
                    d.setSubtotalItem(itemSub);
                    subtotalCalculado = subtotalCalculado.add(itemSub);
                }
            }
            orden.setSubtotal(subtotalCalculado.setScale(2, RoundingMode.HALF_UP));
            BigDecimal igvCalculado = subtotalCalculado.multiply(new BigDecimal("0.18")).setScale(2, RoundingMode.HALF_UP);
            orden.setIgv(igvCalculado);
            orden.setTotal(subtotalCalculado.add(igvCalculado).setScale(2, RoundingMode.HALF_UP));
        } else if (orden.getTotal() != null) {
            // Si vino total directo sin detalles (backward compatibility)
            BigDecimal base = orden.getTotal().divide(new BigDecimal("1.18"), 2, RoundingMode.HALF_UP);
            orden.setSubtotal(base);
            orden.setIgv(orden.getTotal().subtract(base));
        }

        return repository.save(orden);
    }

    @Transactional
    public Optional<Orden> cambiarEstado(Long id, String nuevoEstado) {
        return repository.findById(id).map(o -> {
            o.setEstado(nuevoEstado);
            return repository.save(o);
        });
    }

    public void eliminar(Long id) {
        repository.deleteById(id);
    }
}

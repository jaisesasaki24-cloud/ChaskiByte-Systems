package pe.edu.upeu.catalogo.service;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import pe.edu.upeu.catalogo.entity.Categoria;
import pe.edu.upeu.catalogo.entity.Producto;
import pe.edu.upeu.catalogo.repository.CategoriaRepository;
import pe.edu.upeu.catalogo.repository.ProductoRepository;

import java.math.BigDecimal;

@Component
public class DataInitializer implements CommandLineRunner {

    private final CategoriaRepository categoriaRepo;
    private final ProductoRepository productoRepo;

    public DataInitializer(CategoriaRepository categoriaRepo, ProductoRepository productoRepo) {
        this.categoriaRepo = categoriaRepo;
        this.productoRepo = productoRepo;
    }

    @Override
    public void run(String... args) {
        if (categoriaRepo.count() == 0) {
            Categoria c1 = categoriaRepo.save(Categoria.builder().nombre("Procesadores").descripcion("CPUs Intel y AMD Ryzen para gaming y workstation").activo(true).build());
            Categoria c2 = categoriaRepo.save(Categoria.builder().nombre("Tarjetas Graficas").descripcion("GPUs NVIDIA GeForce RTX y AMD Radeon").activo(true).build());
            Categoria c3 = categoriaRepo.save(Categoria.builder().nombre("Memorias RAM").descripcion("Modulos DDR4 y DDR5 de alta velocidad").activo(true).build());
            Categoria c4 = categoriaRepo.save(Categoria.builder().nombre("Almacenamiento").descripcion("SSDs M.2 NVMe y discos rigidos").activo(true).build());
            Categoria c5 = categoriaRepo.save(Categoria.builder().nombre("Laptops Gamer").descripcion("Equipos portatiles de alto rendimiento").activo(true).build());

            productoRepo.save(Producto.builder().sku("CPU-AMD-001").nombre("AMD Ryzen 7 7800X3D (8C/16T, 5.0GHz)").marca("AMD").precio(new BigDecimal("1780.00")).stockDisponible(15).categoriaId(c1.getId()).imagenUrl("/img/ryzen7800.jpg").build());
            productoRepo.save(Producto.builder().sku("CPU-INT-002").nombre("Intel Core i7-14700K (20C/28T, 5.6GHz)").marca("Intel").precio(new BigDecimal("1850.00")).stockDisponible(10).categoriaId(c1.getId()).imagenUrl("/img/i714700k.jpg").build());
            productoRepo.save(Producto.builder().sku("GPU-NV-001").nombre("NVIDIA GeForce RTX 4070 SUPER 12GB OC").marca("ASUS").precio(new BigDecimal("2950.00")).stockDisponible(8).categoriaId(c2.getId()).imagenUrl("/img/rtx4070s.jpg").build());
            productoRepo.save(Producto.builder().sku("RAM-COR-001").nombre("Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz").marca("Corsair").precio(new BigDecimal("520.00")).stockDisponible(25).categoriaId(c3.getId()).imagenUrl("/img/ram32gb.jpg").build());
            productoRepo.save(Producto.builder().sku("SSD-KIN-001").nombre("Kingston KC3000 2TB PCIe 4.0 NVMe (7000MB/s)").marca("Kingston").precio(new BigDecimal("610.00")).stockDisponible(30).categoriaId(c4.getId()).imagenUrl("/img/ssd2tb.jpg").build());
            productoRepo.save(Producto.builder().sku("LAP-LEN-001").nombre("Lenovo Legion Pro 5 (i7-14700HX, RTX 4060, 16GB, 1TB)").marca("Lenovo").precio(new BigDecimal("5499.00")).stockDisponible(5).categoriaId(c5.getId()).imagenUrl("/img/legion5.jpg").build());
            System.out.println(">>> [ChaskiPC Catalogo] Seed inicial cargado con exito: 5 categorias y 6 productos.");
        }
    }
}

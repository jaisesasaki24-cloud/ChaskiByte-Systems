export interface Producto {
  id: number;
  sku: string;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  categoriaId: number;
  activo: boolean;
}

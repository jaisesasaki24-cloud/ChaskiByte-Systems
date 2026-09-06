export interface DetalleOrden {
  productoId: number;
  nombreProducto: string;
  precioUnitario: number;
  cantidad: number;
  subtotalItem?: number;
}

export interface Orden {
  id?: number;
  codigoOrden?: string;
  cliente: string;
  tipoComprobante: 'BOLETA' | 'FACTURA';
  metodoPago: 'TARJETA' | 'MERCADO_PAGO' | 'YAPE';
  subtotal?: number;
  igv?: number;
  total?: number;
  estado?: string;
  detalles: DetalleOrden[];
}

import 'product.dart';

class CartItem {
  final int id;
  final int productId;
  final int quantity;
  final Product? product;

  CartItem({
    required this.id,
    required this.productId,
    required this.quantity,
    this.product,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    final productJson = (json['product'] as Map?)?.cast<String, dynamic>();
    return CartItem(
      id: json['id'],
      productId: json['product_id'],
      quantity: json['quantity'],
      product: productJson == null ? null : Product.fromJson(productJson),
    );
  }
}

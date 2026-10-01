class Product {
  final int id;
  final String name;
  final String description;
  final int price;
  final String? imageUrl;
  final int categoryId;
  final String categoryName;

  Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    this.imageUrl,
    required this.categoryId,
    required this.categoryName,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    final category = (json['category'] as Map?)?.cast<String, dynamic>();
    return Product(
      id: json['id'],
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      price: json['price'] ?? 0,
      imageUrl: json['image_url'],
      categoryId: category?['id'] ?? 0,
      categoryName: category?['name'] ?? '',
    );
  }
}

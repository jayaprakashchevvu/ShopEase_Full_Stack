import 'package:flutter/material.dart';

import '../models/product.dart';
import '../services/api_service.dart';

class ProductDetailsScreen extends StatelessWidget {
  final Product product;
  final VoidCallback onCartChanged;

  const ProductDetailsScreen({
    super.key,
    required this.product,
    required this.onCartChanged,
  });

  Future<void> addToCart(BuildContext context) async {
    try {
      await ApiService.addToCart(product.id);
      onCartChanged();
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Added to cart')),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString())),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Product details')),
      body: ListView(
        padding: const EdgeInsets.all(18),
        children: [
          AspectRatio(
            aspectRatio: 1,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(18),
              child: product.imageUrl == null
                  ? const Center(child: Icon(Icons.image_outlined, size: 80))
                  : Image.network(
                      ApiService.imageUrl(product.imageUrl),
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) =>
                          const Center(child: Icon(Icons.broken_image_outlined, size: 60)),
                    ),
            ),
          ),
          const SizedBox(height: 22),
          Text(product.name, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(product.categoryName),
          const SizedBox(height: 16),
          Text('₹${product.price}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 18),
          Text(product.description, style: const TextStyle(fontSize: 16, height: 1.5)),
          const SizedBox(height: 28),
          FilledButton.icon(
            onPressed: () => addToCart(context),
            icon: const Icon(Icons.shopping_cart_outlined),
            label: const Text('Add to cart'),
          ),
        ],
      ),
    );
  }
}

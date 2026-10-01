import 'dart:convert';

import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../models/cart_item.dart';
import '../models/category.dart';
import '../models/product.dart';

class ApiService {
  // Android emulator: use 10.0.2.2. iOS simulator/desktop can use 127.0.0.1.
  static const String baseUrl = 'http://10.0.2.2:8000';

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  static Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
  }

  static Future<Map<String, String>> _authHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  static Future<void> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {'username': email, 'password': password},
    );

    if (response.statusCode != 200) {
      throw Exception(_message(response.body, 'Login failed'));
    }

    final data = jsonDecode(response.body);
    await _saveToken(data['access_token']);
  }

  static Future<void> register({
    required String username,
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode != 201) {
      throw Exception(_message(response.body, 'Registration failed'));
    }
  }

  static Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await http.get(
      Uri.parse('$baseUrl/users/me'),
      headers: await _authHeaders(),
    );
    if (response.statusCode != 200) {
      throw Exception('Could not load profile');
    }
    return jsonDecode(response.body);
  }

  static Future<List<Category>> getCategories() async {
    final response = await http.get(Uri.parse('$baseUrl/categories/'));
    if (response.statusCode != 200) {
      throw Exception('Could not load categories');
    }

    return (jsonDecode(response.body) as List)
        .map((item) => Category.fromJson(item))
        .toList();
  }

  static Future<List<Product>> getProducts({int? categoryId, String? search}) async {
    final query = <String, String>{};
    if (categoryId != null) query['category_id'] = '$categoryId';
    if (search != null && search.trim().isNotEmpty) query['search'] = search.trim();

    final uri = Uri.parse('$baseUrl/products/').replace(queryParameters: query);
    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Could not load products');
    }

    return (jsonDecode(response.body) as List)
        .map((item) => Product.fromJson(item))
        .toList();
  }

  static Future<void> addToCart(int productId, {int quantity = 1}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/cart/'),
      headers: await _authHeaders(),
      body: jsonEncode({'product_id': productId, 'quantity': quantity}),
    );

    if (response.statusCode != 200) {
      throw Exception(_message(response.body, 'Could not add item to cart'));
    }
  }

  static Future<List<CartItem>> getCart() async {
    final response = await http.get(
      Uri.parse('$baseUrl/cart/'),
      headers: await _authHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Could not load cart');
    }

    return (jsonDecode(response.body) as List)
        .map((item) => CartItem.fromJson(item))
        .toList();
  }

  static Future<CartItem> updateCart(int cartId, int quantity) async {
    final response = await http.put(
      Uri.parse('$baseUrl/cart/$cartId'),
      headers: await _authHeaders(),
      body: jsonEncode({'quantity': quantity}),
    );

    if (response.statusCode != 200) {
      throw Exception('Could not update cart');
    }
    return CartItem.fromJson(jsonDecode(response.body));
  }

  static Future<void> deleteCartItem(int cartId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/cart/$cartId'),
      headers: await _authHeaders(),
    );
    if (response.statusCode != 200) {
      throw Exception('Could not remove item');
    }
  }

  static Future<Map<String, dynamic>> uploadProfileImage(PlatformFile file) async {
    final token = await getToken();
    if (token == null) throw Exception('Please login again');

    final bytes = await file.readAsBytes();
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/users/profile-image'),
    );
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(
      http.MultipartFile.fromBytes('file', bytes, filename: file.name),
    );

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    if (response.statusCode != 200) {
      throw Exception(_message(response.body, 'Image upload failed'));
    }
    return jsonDecode(response.body);
  }

  static String imageUrl(String? path) {
    if (path == null || path.isEmpty) return '';
    if (path.startsWith('http')) return path;
    return '$baseUrl$path';
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
  }

  static String _message(String body, String fallback) {
    try {
      final data = jsonDecode(body);
      return data['detail']?.toString() ?? fallback;
    } catch (_) {
      return fallback;
    }
  }
}

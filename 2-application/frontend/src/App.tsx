import React, { useState, useEffect } from "react";
import axios from "axios";
import { ShoppingCart, Clock, Search, AlertTriangle } from "lucide-react";

interface Order {
  id: number;
  user_id: number;
  product: string;
  quantity: number;
  total_price: number;
  order_date: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [userId, setUserId] = useState<number>(1);
  const [product, setProduct] = useState<string>("");
  const [quantity, setQuantity] = useState<number>(1);
  const [price, setPrice] = useState<number>(0);
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [discountPercent, setDiscountPercent] = useState<number>(0);
  const [expensiveProducts, setExpensiveProducts] = useState<Order[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get(`${API_URL}/orders/${userId}`);
      setOrders(response.data);
    };
    fetchData();
  }, [userId]);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API_URL}/orders/${userId}`);
      setOrders(response.data);
      setError(null);
    } catch (error) {
      setOrders([]);
      setError("Error fetching orders. Please try again later.");
      console.error(
        "Error fetching orders:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/orders/`, {
        user_id: userId,
        product,
        quantity,
        total_price: price * quantity,
      });

      orders.push(response.data);
      setOrders(orders);
      setProduct("");
      setQuantity(1);
      setPrice(0);
      setError(null);
    } catch (error) {
      setError("Error creating order. Please try again.");
      console.error(
        "Error creating order:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/orders/search?query=${searchQuery}`
      );
      setOrders(response.data);
      setError(null);
    } catch (error) {
      setError("Error searching orders. Please try again.");
      console.error(
        "Error searching orders:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const handleBatchOrder = async () => {
    try {
      const batchOrders = Array(5)
        .fill(null)
        .map(() => ({
          user_id: userId,
          product: `Batch Product ${Math.floor(Math.random() * 1000)}`,
          quantity: Math.floor(Math.random() * 10) + 1,
          total_price: Math.random() * 100,
        }));
      batchOrders.forEach(async (order) => {
        await axios.post(`${API_URL}/orders/`, order);
      });
      setError(null);
      fetchOrders();
    } catch (error) {
      setError("Error creating batch orders. Please try again.");
      console.error(
        "Error creating batch orders:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const fetchUserOrderCounts = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/order_count`);
      console.log("User order counts:", response.data);
      setError(null);
    } catch (error) {
      setError("Error fetching user order counts. Please try again.");
      console.error(
        "Error fetching user order counts:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const fetchAllOrders = async () => {
    try {
      const response = await axios.get(`${API_URL}/all_orders`);
      setOrders(response.data);
      setError(null);
    } catch (error) {
      setError("Error fetching all orders. Please try again.");
      console.error(
        "Error fetching all orders:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const fetchOrderDetails = async (orderId: number) => {
    try {
      const response = await axios.get(
        `${API_URL}/order_details/${orderId}?user_id=${userId}`
      );
      console.log("Order details:", response.data);
      setError(null);
    } catch (error) {
      setError("Error fetching order details. Please try again.");
      console.error(
        "Error fetching order details:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const fetchExpensiveProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/expensive_products`);
      setExpensiveProducts(response.data);
      setError(null);
    } catch (error) {
      setError("Error fetching expensive products. Please try again.");
      console.error(
        "Error fetching expensive products:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  const handleDiscountedOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/orders/create-with-discount`, {
        user_id: userId,
        product,
        quantity,
        price,
        discount_percent: discountPercent,
      });
      setProduct("");
      setQuantity(1);
      setPrice(0);
      setDiscountPercent(0);
      setError(null);
      fetchOrders();
    } catch (error) {
      // Incorrect error handling: not setting error state
      console.error(
        "Error creating discounted order:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  useEffect(() => {
    fetchUserOrders();
  });

  const fetchUserOrders = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/${userId}/orders`);
      setOrders(response.data);
      setError(null);
    } catch (error) {
      setError("Error fetching user orders. Please try again.");
      console.error(
        "Error fetching user orders:",
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">Web Store</h1>

        {error && (
          <div
            className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
            role="alert"
          >
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Create Order</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="userId" className="block mb-1">
                User ID:
              </label>
              <input
                type="number"
                id="userId"
                value={userId}
                onChange={(e) => setUserId(Number(e.target.value))}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            <div>
              <label htmlFor="product" className="block mb-1">
                Product:
              </label>
              <input
                type="text"
                id="product"
                value={product}
                onChange={(e) => setProduct(e.target.value)}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            <div>
              <label htmlFor="quantity" className="block mb-1">
                Quantity:
              </label>
              <input
                type="number"
                id="quantity"
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                className="w-full p-2 border rounded"
                required
                min="1"
              />
            </div>
            <div>
              <label htmlFor="price" className="block mb-1">
                Price per item:
              </label>
              <input
                type="number"
                id="price"
                value={price}
                onChange={(e) => setPrice(Number(e.target.value))}
                className="w-full p-2 border rounded"
                required
                min="0"
                step="0.01"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Create Order
            </button>
          </form>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">
            Create Discounted Order
          </h2>
          <form onSubmit={handleDiscountedOrder} className="space-y-4">
            <div>
              <label htmlFor="discountPercent" className="block mb-1">
                Discount Percent:
              </label>
              <input
                type="number"
                id="discountPercent"
                value={discountPercent}
                onChange={(e) => setDiscountPercent(Number(e.target.value))}
                className="w-full p-2 border rounded"
                required
                min="0"
                max="100"
                step="0.1"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
            >
              Create Discounted Order
            </button>
          </form>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Search Orders</h2>
          <div className="flex space-x-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-grow p-2 border rounded"
              placeholder="Search for products..."
            />
            <button
              onClick={handleSearch}
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              <Search size={20} />
            </button>
          </div>
        </div>

        <div className="space-y-4 mb-8">
          <button
            onClick={handleBatchOrder}
            className="w-full bg-purple-500 text-white p-2 rounded hover:bg-purple-600"
          >
            Create Batch Orders
          </button>
          <button
            onClick={fetchUserOrderCounts}
            className="w-full bg-yellow-500 text-white p-2 rounded hover:bg-yellow-600"
          >
            Fetch User Order Counts
          </button>
          <button
            onClick={fetchAllOrders}
            className="w-full bg-indigo-500 text-white p-2 rounded hover:bg-indigo-600"
          >
            Fetch All Orders (No Pagination)
          </button>
          <button
            onClick={fetchExpensiveProducts}
            className="w-full bg-pink-500 text-white p-2 rounded hover:bg-pink-600"
          >
            Fetch Expensive Products
          </button>
          <button
            onClick={fetchUserOrders}
            className="w-full bg-teal-500 text-white p-2 rounded hover:bg-teal-600"
          >
            Fetch User Orders (With Dependency)
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Order History</h2>
          {orders.length > 0 ? (
            <ul className="space-y-4">
              {orders.map((order) => (
                <li key={order.id} className="border-b pb-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <ShoppingCart className="mr-2" />
                      <span className="font-semibold">{order.product}</span>
                    </div>
                    <div className="text-gray-600">
                      <Clock className="inline mr-1" size={16} />
                      {new Date(order.order_date).toLocaleString()}
                    </div>
                  </div>
                  <div className="mt-2">
                    <span className="text-gray-600">
                      Quantity: {order.quantity}
                    </span>
                    <span className="ml-4 text-gray-600">
                      Total: ${order.total_price.toFixed(2)}
                    </span>
                  </div>
                  <button
                    onClick={() => fetchOrderDetails(order.id)}
                    className="mt-2 bg-gray-200 text-gray-700 px-2 py-1 rounded text-sm hover:bg-gray-300"
                  >
                    View Details
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-600">No orders found for this user.</p>
          )}
        </div>

        {expensiveProducts.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow-md mt-8">
            <h2 className="text-xl font-semibold mb-4">Expensive Products</h2>
            <ul className="space-y-2">
              {expensiveProducts.map((product) => (
                <li
                  key={product.id}
                  className="flex justify-between items-center"
                >
                  <span>{product.product}</span>
                  <span className="font-semibold">
                    ${product.total_price.toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-8 p-4 bg-yellow-100 rounded-lg">
          <h3 className="text-lg font-semibold flex items-center">
            <AlertTriangle className="mr-2" /> Warning: Buggy Application
          </h3>
          <p className="mt-2">
            This application contains intentional bugs for demonstration
            purposes. Be cautious when using these features in a production
            environment.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;

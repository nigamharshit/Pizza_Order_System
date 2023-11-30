import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from app.models import Pizza, PizzaBase, Cheese, Topping, Order
from django.views.decorators.csrf import csrf_exempt
from celery import shared_task

@shared_task
def update_order_status(order_id):
    order = Order.objects.get(pk=order_id)
    # print("function called -> update_order_status")
    # print("Order ID ---> ", order_id, order.status)
    # Update order status based on time elapsed
    if order.status == 'Placed':
        order.status = 'Accepted'
        order.save()
    elif order.status == 'Accepted':
        order.status = 'Preparing'
        order.save()
    elif order.status == 'Preparing':
        order.status = 'Dispatched'
        order.save()
    elif order.status == 'Dispatched':
        order.status = 'Delivered'
        order.save()


def index(request):
    pizzas = Pizza.objects.all()
    pizza_bases = PizzaBase.objects.all()
    cheeses = Cheese.objects.all()
    toppings = Topping.objects.all()
    context = {
        'pizzas': pizzas,
        'pizza_bases': pizza_bases,
        'cheeses': cheeses,
        'toppings': toppings,
    }
    return render(request, 'app/index.html', context)

@csrf_exempt
def generate_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Access the 'pizzas' key from the received data
        pizzas_in_cart = data.get('pizzas', [])

        total_price = 0
        order_details_list = []
        for pizza in pizzas_in_cart:

            pizza_obj = get_object_or_404(Pizza, name=pizza['name'])
            base_obj = get_object_or_404(PizzaBase, pk=pizza['base'])
            cheese_obj = get_object_or_404(Cheese, pk=pizza['cheese'])
            total_price = total_price + pizza_obj.price + base_obj.price + cheese_obj.price
            toppings_list = []
            for toppings in pizza['toppings']:
                topping_obj = get_object_or_404(Topping, pk=toppings)
                total_price = total_price + topping_obj.price
                toppings_list.append(topping_obj.name)
            
            order_details = {
                'selected_pizza': pizza_obj.name,
                'selected_base': base_obj.name,
                'selected_cheese': cheese_obj.name,
                'selected_toppings': toppings_list
            }
            order_details_list.append(order_details)

        new_order = Order.objects.create(
            status='Placed',
            total_price=total_price
        )
        order_id = new_order.order_id  # Retrieve the ID of the newly created order

        # Schedule the task to update order status based on time intervals
        update_order_status.apply_async((order_id,), countdown=30)  # Change status to 'Accepted' after 1 minute
        update_order_status.apply_async((order_id,), countdown=60)  # Change status to 'Preparing' after 1 minute
        update_order_status.apply_async((order_id,), countdown=180)  # Change status to 'Dispatched' after 3 minutes
        update_order_status.apply_async((order_id,), countdown=300)  # Change status to 'Delivered' after 5 minutes

        # Fetch the newly created order
        order = get_object_or_404(Order, pk=order_id)

        # Prepare order details to pass to the template
        order_details = {
            'order_id': order.order_id,
            'status': order.status,
            'total_price': order.total_price,
            'cart_details': order_details_list
        }
 
        # print(order_details_list)
        # print(new_order)
        # print(order_details)

        # Return order_id as JSON response
        return render(request,"app/order_summary.html", {'order_details': order_details})

    return render(request, 'app/index.html')

def get_order_status(request, order_id):
    # print("function Called -> get_order_status")
    order = get_object_or_404(Order, pk=order_id)
    status = order.status
    return JsonResponse({'status': status})






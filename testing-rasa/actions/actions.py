from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os
import uuid

# Suit availibilty action
class ActionCheckSuitAvailability(Action):
    def name(self) -> str:
        return "action_check_suit_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Slots se suit_name aur suit_id nikalna
        suit_name = tracker.get_slot("suit_name")
        suit_id = tracker.get_slot("suit_id")

        # Agar dono slots khali hain, to user se suit name ya ID puchna
        if not suit_name and not suit_id:
            dispatcher.utter_message(text="Mujhe suit ka naam ya ID bataiye taaki main check kar sakoon.")
            return []

        # suit_data.json file se data read karna
        file_path = "suits_data.json"
        if not os.path.exists(file_path):
            dispatcher.utter_message(text="Maaf kijiye, suit data available nahi hai. System mein kuch issue hai.")
            return []

        with open(file_path, "r") as file:
            data = json.load(file)

        # Suit ko dhundna
        suit_found = None
        for suit in data["suits"]:
            # Condition 1: Suit name se match karo
            if suit_name and suit["suit_name"].lower() == suit_name.lower():
                suit_found = suit
                break
            # Condition 2: Suit ID se match karo
            if suit_id and suit["suit_id"] == str(suit_id):  # suit_id string mein hai JSON mein
                suit_found = suit
                break

        # Agar suit mil gaya
        if suit_found:
            if suit_found["availability"]:
                dispatcher.utter_message(
                    text=f"Yeh suit available hai! {suit_found['suit_name']} (ID: {suit_found['suit_id']}) "
                         f"ki price hai {suit_found['price']} PKR. Sizes: {', '.join(suit_found['size'])}. "
                         f"Color: {suit_found['color']}. Image: {suit_found['image_url']}"
                )
            else:
                dispatcher.utter_message(
                    text=f"Maaf kijiye, {suit_found['suit_name']} (ID: {suit_found['suit_id']}) abhi available nahi hai."
                )
        else:
            dispatcher.utter_message(
                text="Maaf kijiye, yeh suit nahi mila. Suit ka naam ya ID dobara check kijiye."
            )

        return []

# place order Action
class ActionPlaceOrder(Action):
    def name(self) -> str:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Slots se user details nikalna
        suit_name = tracker.get_slot("suit_name")
        size = tracker.get_slot("size")
        payment_method = tracker.get_slot("payment_method")
        address = tracker.get_slot("address")
        phone_number = tracker.get_slot("phone_number")

        # Check karo ki sari details hain ya nahi
        if not all([suit_name, size, payment_method, address, phone_number]):
            dispatcher.utter_message(text="Maaf kijiye, order place karne ke liye sari details chahiye. Kya aap dobara check karenge?")
            return []

        # Unique order ID generate karna
        order_id = str(uuid.uuid4())

        # Order object banana
        order = {
            "order_id": order_id,
            "suit_name": suit_name,
            "size": size,
            "payment_method": payment_method,
            "address": address,
            "phone_number": phone_number,
            "status": "pending"  # Order status pending set karna
        }

        # orders.json file mein save karna
        file_path = "orders.json"
        orders = []

        # Agar file pehle se exist karti hai, to usko read karo
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                orders = json.load(file)

        # Naya order add karo
        orders.append(order)

        # File mein save karo
        with open(file_path, "w") as file:
            json.dump(orders, file, indent=4)

        # User ko confirmation message
        dispatcher.utter_message(
            text=f"Apka order place ho gaya hai! Order ID: {order_id}. "
                 f"Suit: {suit_name} , Size: {size}, "
                 f"Payment Method: {payment_method}, Address: {address}, "
                 f"Phone: {phone_number}. Status: Pending."
        )

        return []
# track order action
class ActionTrackOrder(Action):
    def name(self) -> str:
        return "action_track_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Slot se order_id nikalna
        order_id = tracker.get_slot("order_id")

        # Agar order_id nahi hai, to user se puchna
        if not order_id:
            dispatcher.utter_message(text="Maaf kijiye, mujhe apka order ID chahiye taaki main status check kar sakoon.")
            return []

        # orders.json file se data read karna
        file_path = "orders.json"
        if not os.path.exists(file_path):
            dispatcher.utter_message(text="Maaf kijiye, orders ka data available nahi hai. System mein kuch issue hai.")
            return []

        with open(file_path, "r") as file:
            orders = json.load(file)

        # Order ID ke basis pe order dhundna
        order_found = None
        for order in orders:
            if order["order_id"] == order_id:
                order_found = order
                break

        # Agar order mil gaya
        if order_found:
            status = order_found["status"]
            dispatcher.utter_message(
                text=f"Apke order (ID: {order_id}) ka status hai: {status}. "
                     f"Suit: {order_found['suit_name']}, Size: {order_found['size']}, "
                     f"Address: {order_found['address']}."
            )
        else:
            # Agar order nahi mila
            dispatcher.utter_message(
                text="Maaf kijiye, yeh order ID orders mein nahi hai. "
                     "Lagta hai apka dress abhi order nahi hua. Aap dobara order karain, main phir check karta hoon."
            )

        return []
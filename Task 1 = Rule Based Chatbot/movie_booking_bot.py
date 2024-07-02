import random
import re
from datetime import datetime

class MovieBot:
    def __init__(self):
        self.movies = {
            "Avengers: Endgame": ["Action", "Adventure"],
            "Kill Bill : Vol. 1" : ["Action"],
            "SpiderMan : No Way Home" : ["Action", "Adventure"],
            "The Dark Knight Rises": ["Action", "Thriller"],
            "Harakiri" : ["Action", "Drama"],
            "The Godfather": ["Crime", "Drama"],
            "Inception": ["Sci-Fi", "Thriller"],
            "La La Land": ["Musical", "Romance"],
            "The Shawshank Redemption": ["Drama"],
            "2001 : A Space Odyssey": ["Sci-Fi"],
            "The Matrix": ["Action", "Sci-Fi"],
            "Dune Part Two" : ["Action", "Adventure","Sci-Fi"],
            "Blade Runner 2049" : ["Action", "Sci-Fi"],
            "WHIPLASH" : ["Drama", "Music"],
            "Interstellar" : ["Sci-Fi", "Adventure"],
            "The Social Network" : ["Drama"],
        }
        self.theaters = [
            "The Castro Theatre", 
            "New Beverly Cinema" , 
            "PVR Director's Cut" , 
            "Cine Thisio" , 
            "Alamo Drafthouse" , 
            "Cine De Chef"
        ]
        self.showtimes = ["10:00 AM", "12:10 PM", "2:30 PM", "5:20 PM", "8:40 PM", "10:30 PM"]
        self.greetings = [
            "Hello, Welcome to MovieBot! How can I help you?",
            "Hey there! How can I help you today?",
            "Hello movie buff! What's on your mind today?"
        ]
        self.farewells = [
            "Goodbye!", 
            "Have a great day!", 
            "Enjoy your movie!"
        ]
        self.snacks = {
            "Large Popcorn" : 510 ,
            "Medium Popcorn" : 370 , 
            "Small Popcorn" : 210 ,  
            "Soda" : 100, 
            "Nachos with Salsa" : 220, 
            "Hot Dog" : 140 ,
            "Sandwich" : 110 , 
            "Cold Coffee" : 100
        }
        self.snacks_combos = {
            "Lone Ranger": {"items" : ["Medium Popcorn", "Soda"] , "price" : 490}, 
            "Family Pack": {"items" : ["Large Popcorn", "Large Popcorn", "Soda", "Soda", "Soda"], "price" : 720},
            "Unlimited Combo": {"items" : ["Large Popcorn (Refillable)", "Large Soda (Refillable)"], "price" : 610}
        }
        self.ticket_price = {
            "Balcony": 210 , 
            "Gold Class": 145 , 
            "Silver Class": 110
        }
        self.context = {}
        self.chat_history = []
        self.current_step = "greeting"  #initialising the step for the instate conversation.

    def greet(self):
        return random.choice(self.greetings)

    def farewell(self):
        return random.choice(self.farewells)

    def get_movies_by_genre(self, genre):
        return [movie for movie, genres in self.movies.items() if genre in genres]

    def is_weekend(self, date_str):
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date.weekday() >= 5
    
    def calculate_total(self):
        total = self.ticket_price[self.context['ticket_type']] * self.context['tickets']
        if 'snacks' in self.context:
            total += sum(self.snacks[snack] for snack in self.context['snacks'])
        if 'combos' in self.context:
            total += sum(self.snacks_combos[combo]['price'] for combo in self.context['combos'])
        return total

    def generate_ticket(self):
        total = self.calculate_total()
        ticket = f"Movie: {self.context['movie']}\n"
        ticket += f"Theater: {self.context['theater']}\n"
        ticket += f"Date: {self.context['date']}\n"
        ticket += f"Showtime: {self.context['showtime']}\n"
        ticket += f"Ticket Details: {self.context['tickets']} {self.context['ticket_type']} (₹{self.ticket_price[self.context['ticket_type']] * self.context['tickets']})\n"
        
        if 'snacks' in self.context and self.context['snacks']:
            ticket += "Snacks:\n"
            for snack in self.context['snacks']:
                ticket += f"  - {snack} (₹{self.snacks[snack]})\n"
    
        if 'combos' in self.context and self.context['combos']:
            ticket += "Combos:\n"
            for combo in self.context['combos']:
                ticket += f"  - {combo} (₹{self.snacks_combos[combo]['price']})\n"
        
        ticket += f"Total: ₹{total}"
        return ticket

    def get_response(self, user_input):
        user_input = user_input.lower()
        self.chat_history.append(user_input)
        last_message = self.chat_history[-2] if len(self.chat_history) >= 2 else ""

        if self.current_step == "greeting":
            if any(keyword in user_input for keyword in ["hello", "hi", "hey", "hola"]):
                return self.greet()
            elif any(keyword in user_input for keyword in ["book", "movie", "ticket" , "film"]):
                self.current_step = "genre_selection"
                genre_list = ", ".join(set([genre for movie_genres in self.movies.values() for genre in movie_genres]))
                return f"Sure! What genre are you in the mood for? We have: {genre_list}"

        elif self.current_step == "genre_selection":
            genres = set([genre.lower() for movie_genres in self.movies.values() for genre in movie_genres])
            matched_genres = [genre for genre in genres if genre in user_input]
            if matched_genres:
                self.context['genre'] = matched_genres[0].capitalize()
                movies = self.get_movies_by_genre(self.context['genre'])
                if movies:
                    self.context['movie'] = random.choice(movies)
                    self.current_step = "movie_confirmation"
                    return f"How about '{self.context['movie']}'? Would you like to book this movie or see more {self.context['genre'].capitalize()} movie options?"
            else:
                return "I'm sorry, I didn't get that. Please choose a genre from the list."
        
        elif self.current_step == "movie_confirmation":
            if "yes" in user_input:
                self.current_step = "theater_selection"
                return f"Excellent! Which theater would you prefer? We have: {', '.join(self.theaters)}"
            elif any(keyword in user_input for keyword in ["no", "show", "more", "other"]):
                genre_movies = self.get_movies_by_genre(self.context['genre'])
                genre_movies.remove(self.context['movie'])  #to show unique movies other than the previous selected ones.
                if genre_movies:
                    self.context['suggested_movies'] = genre_movies
                    movies_list = ", ".join(genre_movies)
                    return f"Here are some other {self.context['genre']} movies: {movies_list}. Would you like to book any of these?"
            else:
                for movie in self.context.get('suggested_movies' ,[]):
                    if movie.lower() in user_input.lower():
                        self.context['movie'] = movie
                        self.current_step = "theater_selection"
                        return f"Great choice! You have selected this {movie} . Which theater would you prefer? We have: {', '.join(self.theaters)}"

        elif self.current_step == "theater_selection":
            for theater in self.theaters:
                if theater.lower() in user_input:
                    self.context['theater'] = theater
                    self.current_step = "date_selection"
                    return f"Good choice! What date would you like to watch the movie? (Please use DD/MM/YYYY format)"

        elif self.current_step == "date_selection":
            if re.match(r'\d{2}/\d{2}/\d{4}', user_input):
                self.context['date'] = user_input
                self.current_step = "showtime_selection"
                return f"Alright! Here are the available showtimes: {', '.join(self.showtimes)}. Which one do you prefer?"

        elif self.current_step == "showtime_selection":
            for showtime in self.showtimes:
                if showtime.lower() in user_input:
                    self.context['showtime'] = showtime
                    self.current_step = "ticket_selection"
                    return "Great! How many tickets would you like to book?"

        elif self.current_step == "ticket_selection":
            if user_input.isdigit():
                self.context['tickets'] = int(user_input)
                ticket_types = ", ".join([f"{ttype} (₹{price})" for ttype, price in self.ticket_price.items()])
                self.current_step = "ticket_type_selection"
                return f"Perfect! I've booked {self.context['tickets']} tickets. Please choose your ticket type: {ticket_types}"

        elif self.current_step == "ticket_type_selection":
            for ticket_type in self.ticket_price:
                if ticket_type.lower() in user_input:
                    self.context['ticket_type'] = ticket_type
                    self.current_step = "snack_selection"
                    return f"Got it! You've booked {self.context['tickets']} tickets in the {self.context['ticket_type']} section. Would you like to order snacks?"

        elif self.current_step == "snack_selection":
            if "no" in user_input:
                self.current_step = "finalize_order"
                return "Would you like to order anything else? Or proceed to checkout and view your ticket?"

            snack_list = ", ".join([f"{snack} (₹{price})" for snack, price in self.snacks.items()])
            combo_list = ", ".join([f"{combo} (₹{details['price']})" for combo, details in self.snacks_combos.items()])

            if 'snacks' not in self.context:
                self.context['snacks'] = []
            if 'combos' not in self.context:
                self.context['combos'] = []

            for snack in self.snacks:
                if snack.lower() in user_input:
                    self.context['snacks'].append(snack)
                    return f"Great! I've added '{snack}' to your order. Would you like to order anything else?"

            for combo in self.snacks_combos:
                if combo.lower() in user_input:
                    if self.is_weekend(self.context['date']) or "unlimited combo" in combo.lower():
                        self.context['combos'].append(combo)
                        return f"Excellent! I've added the {combo} to your order. Would you like to order anything else?"
                    else:
                        return "I'm sorry, the 'Unlimited Combo' is only available on weekends. Would you like to order something else?"
            return f"We have the following snacks: {snack_list}. We also have the following combos: {combo_list}. What would you like to order?"

        elif self.current_step == "finalize_order":
            if any(keyword in user_input for keyword in ["yes", "checkout", "view ticket"]):
                self.current_step = "ticket_generation"
                return "Great! Your ticket is ready. Would you like to view it?"
            elif "no" in user_input:
                return "Is there anything else I can help you with?"

        elif self.current_step == "ticket_generation":
            if "yes" in user_input:
                return self.generate_ticket()
            elif "no" in user_input:
                return "Is there anything else I can help you with?"

        return "I'm sorry, I didn't understand that. Could you please repeat?"

def chat_with_bot():
    bot = MovieBot()
    print(bot.greet())

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye' , 'thanks' , 'bye' , 'thank you']:
            print("Bot:", bot.farewell())
            break
        response = bot.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    chat_with_bot()
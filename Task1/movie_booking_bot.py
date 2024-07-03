import random
import re
from datetime import datetime
import streamlit as st

class MovieBot:
    def __init__(self):
        self.movies = {
            "The Shawshank Redemption": ["Drama"],
            "Forrest Gump": ["Drama", "Romance"],
            "The Lord of the Rings: The Fellowship of the Ring": ["Adventure", "Fantasy"],
            "The Lion King": ["Animation", "Adventure", "Drama"],
            "Titanic": ["Drama", "Romance"],
            "Jurassic Park": ["Adventure", "Sci-Fi"],
            "Toy Story": ["Animation", "Adventure", "Comedy"],
            "Avatar": ["Action", "Adventure", "Fantasy"],
            "Pulp Fiction": ["Crime", "Drama"],
            "The Silence of the Lambs": ["Crime", "Drama", "Thriller"],
            "Goodfellas": ["Biography", "Crime", "Drama"],
            "The Sixth Sense": ["Drama", "Mystery", "Thriller"],
            "The Usual Suspects": ["Crime", "Mystery", "Thriller"],
            "The Green Mile": ["Crime", "Drama", "Fantasy"],
            "The Pianist": ["Biography", "Drama", "Music"],
            "Life Is Beautiful": ["Comedy", "Drama", "War"],
            "1917" : ["War"],
            "The Grand Budapest Hotel": ["Adventure", "Comedy", "Crime"],
            "Birdman": ["Comedy", "Drama"],
            "Mad Max: Fury Road": ["Action", "Adventure", "Sci-Fi"],
            "The Revenant": ["Action", "Adventure", "Drama"],
            "Whiplash": ["Drama", "Music"],
            "The Martian": ["Adventure", "Drama", "Sci-Fi"],
            "Room": ["Drama", "Thriller"],
            "Spotlight": ["Biography", "Crime", "Drama"],
            "La La Land": ["Comedy", "Drama", "Music"],
            "Moonlight": ["Drama"],
            "Arrival": ["Drama", "Mystery", "Sci-Fi"],
            "Manchester by the Sea": ["Drama"],
            "Get Out": ["Horror", "Mystery", "Thriller"],
            "Annabele" : ["Horror"],
            "Call Me by Your Name": ["Drama", "Romance"],
            "Blade Runner 2049": ["Action", "Drama", "Mystery", "Sci-Fi", "Thriller"],
            "Black Panther": ["Action", "Adventure", "Sci-Fi"],
            "Parasite": ["Comedy", "Drama", "Thriller"],
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
        return [movie for movie, genres in self.movies.items() if genre.lower() in [g.lower() for g in genres]]

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
    

    def parse_snack_order(self, user_input):
        user_input = user_input.lower()
        ordered_snacks = []
        
        quantity_pattern = r'(\d+|a|an|one|two|three|four|five)\s+'
        snack_pattern = r'(large popcorn|medium popcorn|small popcorn|popcorn|soda|nachos|hot dog|sandwich|cold coffee)'
        
        matches = re.findall(f"{quantity_pattern}?{snack_pattern}", user_input)
        
        for match in matches:
            quantity, snack = match
            
            quantity_map = {'a': 1, 'an': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
            quantity = quantity_map.get(quantity, quantity)
            
            quantity = int(quantity) if quantity else 1
            
            snack_map = {
                'popcorn': 'Medium Popcorn',
                'large popcorn': 'Large Popcorn',
                'medium popcorn': 'Medium Popcorn',
                'small popcorn': 'Small Popcorn',
                'soda': 'Soda',
                'nachos': 'Nachos with Salsa',
                'hot dog': 'Hot Dog',
                'sandwich': 'Sandwich',
                'cold coffee': 'Cold Coffee'
            }
            snack = snack_map.get(snack, snack.title())
            
            ordered_snacks.extend([snack] * quantity)
        
        return ordered_snacks

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
            user_input_lower = user_input.lower()
    
    # More flexible matching
            matched_genres = [genre for genre in genres if genre in user_input_lower or user_input_lower in genre]
            if matched_genres:
                self.context['genre'] = matched_genres[0].capitalize()
                movies = self.get_movies_by_genre(self.context['genre'])
                print(f"Debug: Movies in genre: {movies}")  # Debug print
                if movies:
                    self.context['movie'] = random.choice(movies)
                    self.current_step = "movie_confirmation"
                    return f"How about '{self.context['movie']}'? Would you like to book this movie or see more {self.context['genre']} movie options?"
                else:
                    return f"I'm sorry, but we don't have any {self.context['genre']} movies available at the moment. Would you like to try another genre?"
            else:
                return "I'm sorry, I didn't get that. Please choose a genre from the list."
        
        elif self.current_step == "movie_confirmation":
            if "yes" in user_input.lower():
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
                user_input_lower = user_input.lower()
                for movie in self.context.get('suggested_movies' ,[]):
                    if movie.lower() in user_input_lower:
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
            else:
                return "Please enter a valid date in the DD/MM/YYYY format."

        elif self.current_step == "showtime_selection":
            for showtime in self.showtimes:
                if showtime.lower() in user_input:
                    self.context['showtime'] = showtime
                    self.current_step = "ticket_selection"
                    return "Great! How many tickets would you like to book?"
            return "Please choose a valid showtime from the list."

        elif self.current_step == "ticket_selection":
            if user_input.isdigit():
                self.context['tickets'] = int(user_input)
                ticket_types = ", ".join([f"{ttype} (₹{price})" for ttype, price in self.ticket_price.items()])
                self.current_step = "ticket_type_selection"
                return f"Perfect! I've booked {self.context['tickets']} tickets. Please choose your ticket type: {ticket_types}"
            else:
                return "Please Enter a valid number of tickets."

        elif self.current_step == "ticket_type_selection":
            for ticket_type in self.ticket_price:
                if ticket_type.lower() in user_input:
                    self.context['ticket_type'] = ticket_type
                    self.current_step = "snack_selection"
                    return f"Got it! You've booked {self.context['tickets']} tickets in the {self.context['ticket_type']} section. Would you like to order snacks?"
            return "Please choose a valid ticket type."

        elif self.current_step == "snack_selection":
            if "no" in user_input.lower():
                self.current_step = "finalize_order"
                return "Alright, no snacks. Would you like to proceed to checkout and view your ticket?"
            
            if "yes" in user_input.lower() or "sure" in user_input.lower() :
                snack_list = ", ".join([f"{snack} (₹{price})" for snack, price in self.snacks.items()])
                combo_list = ", ".join([f"{combo} (₹{details['price']})" for combo, details in self.snacks_combos.items()])
                return f"Sure! We have the following snacks: {snack_list}. We also have the following combos: {combo_list}. What would you like to order?"

            ordered_snacks = self.parse_snack_order(user_input)
            
            if ordered_snacks:
                if 'snacks' not in self.context:
                    self.context['snacks'] = []
                self.context['snacks'].extend(ordered_snacks)
                snack_summary = ", ".join(f"{ordered_snacks.count(snack)} {snack}" for snack in set(ordered_snacks))
                return f"Great! I've added {snack_summary} to your order. Would you like to order anything else?"
            else:
                snack_list = ", ".join([f"{snack} (₹{price})" for snack, price in self.snacks.items()])
                combo_list = ", ".join([f"{combo} (₹{details['price']})" for combo, details in self.snacks_combos.items()])
                return f"I'm sorry, I didn't catch that. We have the following snacks: {snack_list}. We also have the following combos: {combo_list}. What would you like to order?"

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

USER_AVATAR = "👤"
BOT_AVATAR = "🎥"
def main():
    st.title("Movie Booking Bot")

    if 'movie_bot' not in st.session_state:
        st.session_state.movie_bot = MovieBot()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        bot_greeting = st.session_state.movie_bot.greet()
        st.session_state.messages.append({"role" : "assistant" , "content" : bot_greeting})
    
    for message in st.session_state.messages:
        with st.chat_message(message['role'] ,avatar=BOT_AVATAR if message['role'] == "assistant" else USER_AVATAR):
            st.markdown(message['content'])
    
    if prompt := st.chat_input("What would you like to do today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user",avatar=USER_AVATAR):
            st.markdown(prompt)

        response = st.session_state.movie_bot.get_response(prompt)
        with st.chat_message("assistant",avatar=BOT_AVATAR):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


    if st.session_state.movie_bot.current_step == "ticket_generation":
        ticket = st.session_state.movie_bot.generate_ticket()
        st.markdown("## Your Ticket")
        st.code(ticket, language="text")

if __name__ == "__main__":
    main()
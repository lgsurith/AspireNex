import random
import re
from datetime import datetime, timedelta

#Bot For Movie Booking
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
        self.showtimes = ["10:00 AM , 12:10 AM , 2:30 PM", "5:20 PM", "8:40 PM","10:30 PM"]
        # self.booking = {}
        self.greetings = [
            "Hello , Welcome to MovieBot!. How can I help you ?",
            "Hey There! , How can I help you today?",
            "Hello Movie Buff ! Whats on your mind today ?"
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
            "Sandwhich" : 110 , 
            "Cold Coffee" : 100
        }
        self.snacks_combos = {
            "Lone Ranger ": {"items" : ["Medium Popcorn", "Soda"] , "price" : 490}, 
            "Family Pack ": {"items" : ["Large Popcorns" , " Large Popcorns" , "Soda" , "Soda" , "Soda"],"price" : 720},
            "Unlimited Combo" : {"items" : ["Large Popcorn (Refillable)" , "Large Soda (Refillable)"] , "price" : 610}
        }
        self.ticket_price = {
            "Balcony" : 210 , 
            "Gold Class" : 145 , 
            "Silver Class" : 110
        }
        #making sure to have some history for in chat reference as well as some context for the model to interact.
        self.context = {}   #basically to store all the info about the ticket.
        self.chat_history = []
        self.current_step = "greeting"
    
    def greet(self):
        return random.choice(self.greetings)

    def farewell(self):
        return random.choice(self.farewells)
    
    #to get more movies based on the given genre.
    def get_movies_by_genre(self, genre):
        return [movie for movie, genres in self.movies.items() if genre in genres]

    #functionality for weekend 
    def is_weekend(self, date_str):
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date.weekday() >= 5
    
    #to sum up all the prices.
    def calculate_total(self):
        total = self.ticket_price[self.context['ticket_type']] * self.context['tickets']
        if 'snacks' in self.context:
            total += sum(self.snacks[snack] for snack in self.context['snacks'])
        if 'combos' in self.context:
            total += sum(self.snacks_combos[combo]['price'] for combo in self.context['combos'])
        return total
    
    #to generate the ticket with all the details.
    def generate_ticket(self):
        total = self.calculate_total()
        ticket = f"Movie: {self.context['movie']}\n"
        ticket += f"Theater: {self.context['theater']}\n"
        ticket += f"Date: {self.context['date']}\n"
        ticket += f"Showtime: {self.context['showtime']}\n"
        ticket += f"Ticket Details : {self.context['tickets']} {self.context['ticket_type']} (₹{self.ticket_price[self.context['ticket_type']] * self.context['tickets']})\n"
        if 'snacks' in self.context:
            ticket += "Snacks:\n"
            for snack in self.context['snacks']:
                ticket += f"  - {snack} (₹{self.snacks[snack]})\n"
        if 'combos' in self.context:
            ticket += "Combos:\n"
            for combo in self.context['combos']:
                ticket += f"  - {combo} (₹{self.snacks_combos[combo]['price']})\n"
        ticket += f"Total: ₹{total}"
        return ticket
    
    #to get the response from the user input.
    def get_response(self, user_input):
        user_input = user_input.lower()
        self.chat_history.append(user_input)
        #to make it more context aware and implementing conditional analysis.
        last_message = self.chat_history[-2] if len(self.chat_history) >= 2 else ""

        #setting up context for the greeting as well as natural repsonse in bopking a movie.
        if self.current_step == "greeting":
            greeting_keywords = ["hello" , "hi" , "hey" , "hola" ]
            booking_greeting_keywords = ["hey" , "hi" , "i" , "want" , "book" , "movie" , "tickets" , "ticket"]
            if any(keyword in user_input for keyword in greeting_keywords):
                self.current_step = "greeting"
                return f"{random.choice(self.greetings)}"
            elif any(keyword in user_input for keyword in booking_greeting_keywords):
                self.current_step = "genre_selection"
                return "Great! I can help you book a movie. What genre are you interested in?"
        
        #to get the genre of the movie.
        elif self.current_step == "genre_selection":
            genre_keywords = ["genre" , "type of movies" , "type" , "genre of a movie"]
            if any (keyword in user_input for keyword in genre_keywords):
                movies = [movie for movie , movie_genre in self.movies.items() if any (genre.lower() in user_input for genre in movie_genre)]
                if movies:
                    self.context['movie'] = random.choice(movies)
                    self.context['genre'] = next(genre for genre in self.movies[self.context['movie']] if genre.lower() in user_input)
                    self.current_step = "movie_confirmation"
                    return f"Aamzing choice! How about '{self.context['movie']}'? Would you like to book this movie or see more {self.context['genre']}  movie options?"
        

                          




        if any(word in user_input for word in ["hello", "hi", "hey"]): 
            return f"{random.choice(self.greetings)}"

        elif "book" in user_input and "movie" in user_input and "ticket" in user_input:
            return "Great! I can help you book a movie. What genre are you interested in?"

        elif "genre" in user_input or "type of movie" in user_input:
            genres = set(genre for movie_genres in self.movies.values() for genre in movie_genres)
            return f"We have movies in the following genres: {', '.join(genres)}. Which genre would you like?"
        
        elif "snack" in user_input or "snacks" in user_input or "food" in user_input:
            snack_list = ", ".join([f"{snack} (₹{price})" for snack, price in self.snacks.items()])
            combo_list = ", ".join([f"{combo} (₹{details['price']})" for combo, details in self.snacks_combos.items()])
            return f"We have the following snacks: {snack_list}. We also have the following combos: {combo_list}. Would you like to order anything?"
        
        elif any(snack.lower() in user_input for snack in self.snacks):
            ordered_snack = next(snack for snack in self.snacks if snack.lower() in user_input)
            if 'snacks' not in self.context:
                self.context['snacks'] = []
            self.context['snacks'].append(ordered_snack)
            return f"Great! I've added '{ordered_snack}' to your order. Would you like to order anything else?"

        elif any(combo.lower() in user_input for combo in self.snacks_combos):
            ordered_combo = next(combo for combo in self.snacks_combos if combo.lower() in user_input)
            if self.is_weekend(self.context['date']) or "Unlimited Combo" in ordered_combo:
                if 'combos' not in self.context:
                    self.context['combos'] = []
                self.context['combos'].append(ordered_combo)
                return f"Great! I've added the '{ordered_combo}' to your order. Would you like to order anything else?"
            else:
                return "I'm sorry, the 'Unlimited Combo' is only available on weekends. Would you like to order something else?"
        
        # elif any(genre.lower() in user_input for genre in set(genre for movie_genres in self.movies.values() for genre in movie_genres)):
        #     matching_movies = [movie for movie, genres in self.movies.items() if any(genre.lower() in user_input for genre in genres)]
        #     if matching_movies:
        #         self.context['movie'] = random.choice(matching_movies)
        #         return f"Great choice! How about '{self.context['movie']}'? Would you like to book this movie?"

        elif any(genre.lower() in user_input for genre in set(genre for movie_genres in self.movies.values() for genre in movie_genres)):
            matching_movies = [movie for movie , genres in self.movies.items() if any(genre.lower() in user_input for genre in genres)]    
            if matching_movies:
                self.context['movie'] = random.choice(matching_movies)
                selected_genre = next(genre for genre in self.movies[self.context['movie']] if genre.lower() in user_input)
                self.context['genre'] = selected_genre
                return f"Great choice! How about '{self.context['movie']}'? It's a fantastic {selected_genre} film! Would you like to book this movie or see more {selected_genre} options?"

        elif "show me more" in user_input and "movies" in user_input and "genre" in user_input and "any other" in user_input:
            genre = self.context.get('genre')
            if genre:
                genre_movies = self.get_movies_by_genre(genre)
                if genre_movies:
                    genre_movies.remove(self.context['movie'])
                    if genre_movies:
                        movie_list = ", ".join(genre_movies)
                        return f"Here are some other {genre} movies: {movie_list}. Would you like to book any of these?"
                    else:
                        return f"I'm sorry, there are no other {genre} movies. Would you like to book this movie instead?"
                

        elif "yes" in user_input and 'movie' in self.context:
            return f"Excellent! Which theater would you prefer? We have: {', '.join(self.theaters)}"
        
        elif "yes" in user_input  and 'order' in last_message:
            return "What can i get for you ?"
        
        elif "yes" in  user_input and 'snack' in last_message:
            return "Which snack would you like to order?"
        
        elif "yes" in user_input and 'combo' in last_message:
            return "Which combo would you like to order?"

        elif any(theater.lower() in user_input for theater in self.theaters):
            self.context['theater'] = next(theater for theater in self.theaters if theater.lower() in user_input)
            return f"Good choice! What date would you like to watch the movie? (Please use DD/MM/YYYY format)"

        elif re.match(r'\d{2}/\d{2}/\d{4}', user_input):
            self.context['date'] = user_input
            return f"Alright! Here are the available showtimes: {', '.join(self.showtimes)}. Which one do you prefer?"

        elif any(showtime.lower() in user_input for showtime in self.showtimes):
            self.context['showtime'] = next(showtime for showtime in self.showtimes if showtime.lower() in user_input)
            return "Great! How many tickets would you like to book?"

        elif user_input.isdigit():
            self.context['tickets'] = int(user_input)
            ticket_type = ", ".join([f"{ticket_type} (₹{price})" for ticket_type, price in self.ticket_price.items()])
            return f"Perfect! I've booked {self.context['tickets']} tickets. Please choose your ticket type: {ticket_type}"
        
        elif any(ticket_type.lower() in user_input for ticket_type in self.ticket_price):
            self.context['ticket_type'] = next(ticket_type for ticket_type in self.ticket_price if ticket_type.lower() in user_input)
            return f"Got it! You've booked {self.context['tickets']} tickets in the {self.context['ticket_type']} section. Would you like to order snacks?"

        elif "thank" in user_input or "thank you" in user_input:
            return self.farewell()
        
        elif "ticket" in user_input:
            return self.generate_ticket()

        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"

def chat_with_bot():
    bot = MovieBot()
    print(bot.greet())

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot:", bot.farewell())
            break
        response = bot.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    chat_with_bot()
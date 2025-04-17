import string
from tkinter import *
from abc import ABC, abstractmethod
import random
import os
import json

#GAME BLUEPRINTS IMPLEMENTATION REQUIREMENTS
class GameABC(ABC):

    @abstractmethod
    def init_screen(self) -> None:
        """HERE WHERE THE GAME DESIGN IMPLEMENTED !Should apply with the main class.
        Inherit Tk in th
        """
        pass
    @abstractmethod
    def load_progress(self) -> None:
        """For data game progress (JSON File)
        Data should load and apply in instance variable of game class
        """
        pass
    @abstractmethod
    def update_level(self) -> None:
        """ move to the next level of the game after user guessed the answer
        """
        pass
    @abstractmethod
    def shuffle_ans(self) -> list[str]:
        """Here where the answer of particular images should in random arrangement letter
        using random method
        """
        pass

    @abstractmethod
    def skip_level(self) -> None:
        """skip to the next level"""
        pass
    @abstractmethod
    def hint(self,b) -> None:
        """will provide each letter in answer box"""
        pass
    @abstractmethod
    def check_answer(self) -> None:
        ""
        pass
#INITIALIZATION OF GAME DESIGN WITH FUNCTIONALITY
class Game(Tk,GameABC):
    # name of filename data
    __DATA_FILENAME = f"{os.path.dirname(__file__)}\\progress_data.json"
    __DATA_IMAGE_NAME = f"{os.path.dirname(__file__)}\\level_list.txt"

    #container for all answer list and image name
    __answerList = []
    __imageNameList = []

    # LOAD PROGRESS OF THE GAME
    def save_progress(self,data):
        try:
            with open(self.__DATA_FILENAME,'w') as file :
                json.dump(data,file)
        except FileNotFoundError:
            pass
    def load_progress(self) -> None:
        try:
            with open(self.__DATA_FILENAME,'r') as file :
                data = json.load(file)
                self.imageNum = data['pic_num']
                self.correct = data['answer']
                self.coin_count = data['coins']
        except FileNotFoundError:
            # initialize default value of properties game progress if json file not defined yet
            self.imageNum = 0 # Default level + 1
            self.correct = ""
            self.coin_count = 50
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.title("4 Pics 1 Word")
        self.resizable(False,False)

        self.init_screen()
        
    # ALL WIDGET IS INITIALIZE HERE
    def init_screen(self) -> None:
        def load_entities():
            """This method is for getting all possible answer list per level
             and also process rearranging list of item answers"""
            self.load_progress()
            try:
                if os.path.exists(self.__DATA_FILENAME):
                    with open(self.__DATA_IMAGE_NAME, 'r') as file:
                        for item in file.readlines():
                            temp = item.strip().split(';')
                            # get each line of answer and name list ex: 1;war -> war : target data to store in two instance below
                            self.__answerList.append(temp[1])
                            self.__imageNameList.append(temp[1])
                else:
                    with open(self.__DATA_IMAGE_NAME, 'r') as file1:
                        lines = [i.strip().split(';') for i in file1.readlines()]
                        names = [name[1] for name in lines]
                        random.shuffle(names)
                    with open(self.__DATA_IMAGE_NAME, 'w') as file2:
                        for index, name in enumerate(names):
                            file2.write(f"{index + 1};{name}\n")
                            self.__imageNameList.append(name)
                            self.__answerList.append(name)
                if self.imageNum is None:
                    self.imageNum = 0

                else:
                    self.imageNum = self.imageNum

                self.correct = self.__answerList[self.imageNum]
            except FileNotFoundError:
                print("Error: File not found (Failed to load progress data)")
            except IndexError:
                self.imageNum = 0 
                self.coin_count = 100
                self.correct = self.__answerList[self.imageNum]
        load_entities()     
        
        main_color_bg = "#152238"
        self.background_frame = Frame(self,name='bg_frame',width=500,height=700,bg=main_color_bg)
        self.background_frame.pack()
        self.background_frame.place(x=0,y=0)

        gs_bg_color = "#4682B4"
        self.game_status = Frame(self.background_frame,name="stats_bar",bg=gs_bg_color,width=500,height=65)
        self.game_status.pack()
        self.game_status.place(x=0,y=0)


        self.level = Label(self.game_status,text=f"Level {str(self.imageNum+1)}",name="current_level",bg=gs_bg_color,font=('Courier',14,"bold"),fg='white')
        self.level.pack()
        self.level.place(x=18,y=19)
        
        self.coin_img = PhotoImage(file=f"{os.path.dirname(__file__)}\\pics\\coin2.png").subsample(16)
        self.coin = Label(self.game_status,image=self.coin_img,bg=gs_bg_color)
        self.coin.pack()
        self.coin.place(x=380,y=15)

        self.coin_status = Label(self.game_status,name="coin_status",text=self.coin_count,bg=gs_bg_color,font=("Courier",14,"bold"), fg='white')
        self.coin_status.pack()
        self.coin_status.place(x=420, y=19)

        self.game_img_frame = Frame(self,name="game_img_frame",width=400,height=340)
        self.game_img_frame.pack()
        self.game_img_frame.place(x=50,y=105)

        self.guess_img = PhotoImage(file=f"{os.path.dirname(__file__)}"+r"\\pics\\{}.png".format(self.__imageNameList[self.imageNum]))
        self.label_pic = Label(self.game_img_frame,image=self.guess_img,width=400,height=340,bg=main_color_bg)
        self.label_pic.pack()
        self.label_pic.place(x=0,y=0)

        self.btn_frame = Frame(self,width=300,height=130,bg=main_color_bg)
        self.btn_frame.pack()
        self.btn_frame.place(x=100,y=530)

        self.hint_img = PhotoImage(file=f"{os.path.dirname(__file__)}\\pics\\hint.png").subsample(10)
        self.hint_btn = Button(self,width=35,height=35,image=self.hint_img,borderwidth=0,activebackground=main_color_bg,bg=main_color_bg)
        self.hint_btn.config(command= lambda b=self.hint_btn: self.hint(b))
        self.hint_btn.place(x=422,y=533)

        self.next_img = PhotoImage(file=f"{os.path.dirname(__file__)}\\pics\\next.png").subsample(25)
        self.next_label = Button(self, width=40, height=40, image=self.next_img,borderwidth=0,activebackground=main_color_bg,bg=main_color_bg)
        self.next_label.config(command=self.skip_level)
        self.next_label.place(x=420, y=590)

        self.ans_box_frame = Frame(self,name='ans_frame',width=400, height=60,bg=main_color_bg)
        self.ans_box_frame.pack()
        self.ans_box_frame.place(relx=0.5,y=475, anchor="center")

        self.is_user_used_hint = False
        self.ans_current_answer = []
        self.current_btn_used = []
        self.init_buttons()
        self.init_placeholder()
    # ANSWER PLACEHOLDER PROPERTIES
    def init_placeholder(self):
        self.display_guess = [''] * len(self.correct)
        for i in range(len(self.display_guess)):
            self.ans_box = Label(self.ans_box_frame, text="", width=4, height=2, bg="white", relief="ridge",
                                 font="Arial 12 bold")
            self.ans_current_answer.append(self.ans_box)
            self.ans_box.pack(side=LEFT, padx=1)
            self.ans_current_answer[i].bind('<Button-1>', lambda event, index=i: self.remove_ans_on_click_label(index))
    # BUTTON PROPERTIES
    def init_buttons(self):
        for i, letter in enumerate(self.shuffle_ans()):
            self.letter_btn = Button(self.btn_frame, text=letter, font=('Arial', 13), width=4, height=2)
            self.letter_btn.config(command=lambda l=letter, btn=self.letter_btn: self.on_click_btn(l, btn))
            self.letter_btn.grid(row=i // 6, column=i % 6, padx=2, pady=2)
    # 
    def init_next_screen(self):
        self.next_level_frame = Frame(self,width=500,height=700-65,bg="#152238")
        self.next_level_frame.pack(side=BOTTOM)
        self.next_level_frame.place(x=0,y=65)

        self.message_label = Label(self.next_level_frame,text="Very Good!",font="Arial 32 bold",fg="yellow",bg="#152238")
        self.message_label.pack()
        self.message_label.place(x=int(self.winfo_width())//3.8,y=170)
        
        self.final_ans_label = Label(self.next_level_frame,text="Correct answer",width=20,height=4,font="Arial 12 bold",bg="#152238",fg="white")
        self.final_ans_label.pack()
        self.final_ans_label.place(relx=.5,y=310,anchor=CENTER)
        
        self.final_ans_label = Frame(self.next_level_frame,width=350,height=70,bg="#152238")
        self.final_ans_label.pack()
        self.final_ans_label.place(relx=0.5,y=360, anchor="center")
        for i in self.correct:
            self.final_ans = Label(self.final_ans_label, text=f"{i.upper()}", width=4, height=2, bg="white", fg="green",relief="ridge",
                                 font="Arial 14 bold")
            self.final_ans.pack(side=LEFT, padx=1)

        self.next_btn = Button(self.next_level_frame,text="Next Level",width=10,height=1,font="Arial 14 bold",bg="#101b2f",fg="white")
        def m():
            self.next_level_frame.destroy()
            if self.imageNum < 49:
                self.init_screen()
            else :
                self.init_completed()
        self.next_btn.config(command=m)
        self.next_btn.pack()
        self.next_btn.place(x=int(self.winfo_width())//2.67,y=470)
    #
    def init_completed(self):
        self.celeb_frame = Frame(self,width=500,height=700)
        self.celeb_frame.pack()
        self.celeb_frame.place(x=0,y=0)
        
        self.celeb_img = PhotoImage(file=f'{os.path.dirname(__file__)}\\pics\\celeb.png').subsample(5)
        
        self.celeb_label = Label(self.celeb_frame,image=self.celeb_img)
        self.celeb_label.pack()
        self.celeb_label.place(anchor=CENTER,relx=.5,rely=.5)
        
        self.e_text = Label(self.celeb_frame,text="Congratulations!",width=30,height=5,font="Arial 18 bold", fg="Red",bg="#fffff4")
        self.e_text.pack()
        self.e_text.place(anchor=CENTER,relx=.5,rely=.5)
    
    # FUNCTION TO PERFORM IF THE BUTTON IS CLICKED  
    def on_click_btn(self,c,btn):
        self.current_btn_used.append(btn)

        for i in self.ans_current_answer:
            if len(i.cget('text')) < 1 :
                i.config(text=f"{c}")
                break
        ans_length = len("".join(i.cget('text') for i in self.ans_current_answer))

        if ans_length == len(self.correct):
            self.check_answer()
            return
        self.disable_btn(btn)
    # SIMPLE METHOD TO DISABLE BTN
    @staticmethod
    def disable_btn(btn):
        "To disabled defined instance button"
        btn.config(state=DISABLED)
    # FUNCTION OF REMOVING PARTICULAR LABEL WHEN CLICKED
    def remove_ans_on_click_label(self,l):
        current_label = self.ans_current_answer[l]
        for i in self.current_btn_used:
            if i.cget('text') == current_label.cget('text'):
                if current_label.cget('fg') != "green":
                    current_label.config(text="")
                    i.config(state=NORMAL)
    # FUNCTION THAT VALIDATE IF THE CURRENT ANSWER IS EQUAL TO THE CORRECT ANSWER
    def check_answer(self) -> None:
        if self.correct.upper() == "".join(i.cget('text') for i in self.ans_current_answer):
            self.coin_count += 5 if self.is_user_used_hint else 10
            self.update_level()
        else:

            self.ResetMainEntities()
    # FUNCTION OF SKIPPING NEXT LEVEL WITH THE COST OF 10 COINS
    def skip_level(self) -> None:
        COIN_COST = 10
        def skip():
            if self.coin_count >= COIN_COST:
                self.coin_count -= COIN_COST
                self.coin_status.config(text=self.coin_count)
                self.update_level()
        self.confirmation(coin_cost=COIN_COST,type="Skip",func=skip)
    # FUNCTION OF GIVING RANDOM LETTER ANSWER TO BOX PLACEHOLDER WITH COST OF 2 COINS EACH HINT
    def hint(self,b) -> None:
        "Every click of the Hint button interface this program will trigger "
        COIN_COST = 2
        def hint_func() -> bool:
            ans_box = self.ans_current_answer
            ans_length = len("".join(i.cget('text') for i in ans_box))
            
            if self.coin_count >= COIN_COST:
                self.hint_frame.destroy()
                
                while True and ans_length != len(ans_box):
                    #Generate random letter in the correct answer
                    ran_index = random.randint(0, len(self.correct) - 1)
                    hint_letter = self.correct[ran_index].upper()

                    #Check if the length of label box determined by random number is EMPTY, otherwise it will loop until get the particular text len == 0
                    if not len(ans_box[ran_index].cget('text')) > 0:
                        #Get all children button instance of btn_frame
                        buttons = self.btn_frame.winfo_children()

                        #Disable button with the state=normal and equal to the hint_letter
                        for i,btn in enumerate(buttons):
                            if btn.cget('text') == hint_letter and btn.cget('state') == "normal":
                                self.is_user_used_hint = True
                                self.disable_btn(btn)
                                break
                        #
                        ans_box[ran_index].config(text=hint_letter, fg="green")
                        self.coin_count -= COIN_COST
                        self.coin_status.config(text=self.coin_count)
                        
                        self.check_answer()
                        return True
            else:
                return False
        self.confirmation(coin_cost=COIN_COST,type="Hint",func=hint_func)
    #
    def confirmation(self,func=None,**kwargs):
        
        self.hint_frame = Frame(self,width=300,height=300/2,bg="#152238",highlightthickness=2,highlightbackground="white")
        self.hint_frame.pack()
        self.hint_frame.place(anchor=CENTER,relx=.5,rely=.5)
        
        self.hint_text = Label(self.hint_frame,text=f"Are you sure you want to use {kwargs.get('type')}?",width=30,height=3,font="Arial 11 bold",fg="white",bg="#152238")
        self.hint_text.pack()
        self.hint_text.place(x=7,y=1)
        
        self.hint_text_cost = Label(self.hint_frame,text=f"{kwargs.get('coin_cost')} Cost",width=5,height=1,font="Arial 12 bold",fg='white',bg="#152238")
        self.hint_text_cost.pack()
        self.hint_text_cost.place(x=300//2.1,y=55)
        
        self.deduction_coin = Label(self.hint_frame,image=self.coin_img,width=30,height=30,bg="#152238")
        self.deduction_coin.pack()
        self.deduction_coin.place(x=300/3,y=50)
        
        self.y_btn = Button(self.hint_frame,text="Yes",width=8,height=1,command=func)
        self.y_btn.pack()
        self.y_btn.place(x=300/5,y=105)
        
        if int(self.coin_count) < kwargs.get('coin_cost'):
            self.y_btn.config(state=DISABLED)
            self.hint_text_cost.config(fg="red")
        
        self.n_btn = Button(self.hint_frame,text="No",width=8,height=1 , command=self.hint_frame.destroy)
        self.n_btn.pack() 
        self.n_btn.place(x=300/1.8,y=105)
        
    #UPDATE GAME PROGRESS DATA
    def update_level(self) -> None:
        
        data = {
                "pic_num": self.imageNum+1,
                'answer': "",
                'coins': self.coin_count
            }
        self.save_progress(data)
        self.init_next_screen()
        return
    # FUNCTION OF RESETTING THE KEY BUTTON AND LABEL IF WRONG ANSWER AND EXCEED IN THE MAX LENGTH OF LABEL LIST
    def ResetMainEntities(self):
        try:
            if len(self.current_btn_used) == len(self.correct):
                for i, d in enumerate(self.ans_current_answer):
                    if d.cget('fg') != "green":
                        d.config(text="")
                        self.current_btn_used[i].config(state=NORMAL)

                self.current_btn_used.clear()
        except IndexError:
            return
    # RETURN LIST OF SHUFFLE CORRECT ANSWER INTO PRECEDING POSITION
    def shuffle_ans(self) -> list[str]:
        answer = list(self.correct.upper())
        more_letter = random.choices(string.ascii_uppercase, k=max(12 - len(answer), 0))
        final_letter = answer + more_letter
        random.shuffle(final_letter)

        return final_letter



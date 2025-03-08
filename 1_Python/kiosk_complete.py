#키오스크
# 필요한 조건
# 햄버거 선택 -> 추가,제거 재료 선택-> 햄버거 선택..... 햄버거 선택 창에서 결제 ->매장, 포장 선택 ->결제수단 선택 ->주문표 및 영수증 출력
# 
# 완성-> 주문 종료후 초기화면 돌아가기, 재료 계속 추가 또는 제거 가능, 돌아가기 기능 가능, 


# for문으로 반복 if문 줄일 수 있을듯듯



# 입력받은 데이터 검증 및 int로 변환
def data_chek(num):
    if len(num): isok=True
    else: isok=False
    if num.isdecimal():
        return isok
    else: isok=False




# 0(메인화면) ->1주문 ->1.2 메뉴선택-메뉴당 재료추가+제거 옵션, (선택한 메뉴 보여주기 및 선택한 메뉴 제거)
                # ->1.3 ->포장, 매장식사 선택 -> (포인트 적립여부 묻기))-> 결제 -> 영수증 출력여부->영수증 및 번호표 출력
            # -->직원호출시 기다려 달라는 문구

#햄버거 클래스
intgred= ['패티', '양상추', '토마토', '치즈', '피클']
class Hamburger:                                    
    def __init__(self, price, burger_name):
        self.price = price
        self.burger_name = burger_name
        self.ingredients = intgred

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
        else:
            print(f"{ingredient} 을/를 {self.burger_name}에 제거할 수 없습니다.")

    def display_info(self):
        if menu_set==True:
            print(f"제품이름: {self.burger_name} 세트")
        else:
            print(f"제품이름: {self.burger_name}")
        print(f"가격: {self.price} 원")
        print("재료(기본='패티', '양상추', '토마토', '치즈', '피클'):")
        for ingredient in self.ingredients:
            print(f"- {ingredient}")

# 햄버거 객체 생성
whopper = Hamburger(8000, "와퍼")
cheese_whopper = Hamburger(8600, "치즈와퍼")
bulgogi_whopper = Hamburger(8000, "불고기 와퍼")
shirimp_whopper = Hamburger(8800, "통새우 와퍼")
bulgogi_burger = Hamburger(4900, "불고기버거")
bc_cheese_whopper = Hamburger(9800, "베이컨치즈와퍼")



# 메인화면 ->(1. 주문하기    2.직원호출)
def print_main_menu():
    print(f'{"*":*^19}')
    print(f'{"     버  거  킹":19}')
    print(f'{"*":*^19}')
    print(f'{"*  1  주문  하기  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  2  직원  호출  *":19}')
    print(f'{"*":*^19}')

# 주문 화면  --글자 + :17==19가 되도록
def print_menu():
    print(f'{"*":*^19}',end=' '), print(f'{"*":*^19}')
    print(f'{"*  1  와     퍼   *":17}',end=' '), print(f'*{whopper.price:^15}원*')
    print(f'{"*  2  불고기 와퍼 *":12}',end=' '), print(f'*{bulgogi_whopper.price:^15}원*')
    print(f'{"*  3  치즈  와퍼  *":15}',end=' '), print(f'*{cheese_whopper.price:^15}원*')
    print(f'{"*  4  통새우 와퍼 *":13}',end=' '), print(f'*{shirimp_whopper.price:^15}원*')
    print(f'{"*  5  불고기 버거 *":14}',end=' '), print(f'*{bulgogi_burger.price:^15}원*') 
    print(f'{"*  6베이컨치즈와퍼*":11}',end=' '), print(f'*{bc_cheese_whopper.price:^15}원*')
    print(f'{"*":*^19} {"*":*^19}')


# 1-2. 선택한 재료 추가/제거 화면
def print_addition_1():
    print(f'{"*":*^19}')
    print(f'{"*  1  재료  추가  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  2  재료  빼기  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  3  취      소  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  4  완      료  *":19}')
    print(f'{"*":*^19}')

# 1-1. 추가/제거할 재료 선택 화면
def print_addition_():
    print(f'{"*":*^19} {"*":*^19}',)
    print(f'{"*  1  패     티   *":17} {"*  2  양  상  추  *":18}')
    print(f'{"*":*^19} {"*":*^19}')
    print(f'{"*  3  치     즈   *":17} {"*  4  토  마  토  *":18}')
    print(f'{"*":*^19} {"*":*^19}')
    print(f'{"*  5  피     클   *":17} {"*  6  뒤로  가기  *":15}')


# 세트 선택 여부
def print_set():
    print(f'{"*":*^19}')
    print(f'{"*  1  세      트  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  2  단      품  *":19}')
    print(f'{"*":*^19}')

#2-  포장/매장 식사 선택
def print_take():
    print(f'{"*":*^19}')
    print(f'{"*  1  포      장  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  2  매장  식사  *":19}')
    print(f'{"*":*^19}')
#3-  결제 수단 선택

def print_pay():
    print(f'{"*":*^19}')
    print(f'{"*  1  카      드  *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  2  현      금  *":19}')
    print(f'{"*":*^19}')
# 4- 영수증 및 번호표 출력
def print_reciept():
    print(f'{"*":*^19}')
    print(f'{"*  영  수   증  ○ *":19}')
    print(f'{"*":*^19}')
    print(f'{"*  영  수   증  X *":19}')
    print(f'{"*":*^19}')
    '영수증'






# 키오스크 시작
x=1
while True:
    reset=False
    print_main_menu()       #메인 화면
    choice_main = (input('메뉴 선택: '))                   #인풋1. 메인화면
    check=True
    if data_chek(choice_main):
        choice_main= int(choice_main)
    else: check=False
    if choice_main==2: staff=input('직원을 호출하였습니다 잠시만 기다려 주세요.');continue
    elif choice_main==1:
        # order=[]    
        while True:
            order=[]

            while True:                                     #햄버거 주문
                print_menu()
                choice_menu= input('메뉴를 선택해 주세요')             #인풋2. 햄버거 주문
                check=True
                if data_chek(choice_menu):
                    choice_menu= int(choice_menu)
                else: check=False
                if choice_menu==1:
                    burger = whopper
                elif choice_menu==2:
                    burger = Hamburger(8000, "불고기 와퍼")
                elif choice_menu==3:
                    burger = Hamburger(8600, "치즈와퍼")
                elif choice_menu==4:
                    burger = Hamburger(8800, "통새우 와퍼")
                elif choice_menu==5:
                    burger = Hamburger(4900, "불고기버거")
                elif choice_menu==6:
                    burger = Hamburger(9800, "베이컨치즈와퍼")
                elif check==False: print(f'{choice_menu}는 올바르지 않은 번호입니다.');continue
                else: print(f'{choice_menu}는 올바르지 않은 번호입니다.');continue
                
                ing_bool=True
                while ing_bool:
                    print(f'{burger.burger_name}을(를) 선택하셨습니다')           #재료 추가/제거 선택
                    print_addition_1()
                    extra= input('재료의 추가/제거 여부를 선택해 주세요')   #인풋3. 재료 추가
                    check=True
                    if data_chek(extra):
                        extra= int(extra)
                    else: check=False
                    if extra==1:
                        while True:
                            print_addition_()
                            choice_ing= input('추가/제거할 재료를 선택하세요')     #인풋4. 추가할 재료 선택//
                            check=True
                            if data_chek(choice_ing):
                                choice_ing= int(choice_ing)
                            else: check=False
                            if choice_ing==1:
                                burger.add_ingredient('패티')
                            elif choice_ing==2:
                                burger.add_ingredient('양상추')
                            elif choice_ing==3:
                                burger.add_ingredient('치즈')
                            elif choice_ing==4:
                                burger.add_ingredient('토마토')
                            elif choice_ing==5:
                                burger.add_ingredient('피클') 
                            elif choice_ing==6:
                                print('이전 화면으로 돌아갑니다')
                                break
                            elif check==False: print(f'{choice_ing}는 올바르지 않은 번호입니다.');continue
                            else: print(f'{choice_ing}는 올바르지 않은 번호입니다.');continue
                    elif extra==2:
                        while True:
                            print_addition_()
                            choice_ing= input('추가/제거할 재료를 선택하세요')   #인풋5. 재료 제거//
                            check=True
                            if data_chek(choice_ing):
                                choice_ing= int(choice_ing)
                            else: check=False                        #제거할 재료 선택
                            if choice_ing==1:
                                burger.remove_ingredient('패티')
                            elif choice_ing==2:
                                burger.remove_ingredient('양상추')
                            elif choice_ing==3:
                                burger.remove_ingredient('치즈')
                            elif choice_ing==4:
                                burger.remove_ingredient('토마토')
                            elif choice_ing==5:
                                burger.remove_ingredient('피클') 
                            elif choice_ing==6:
                                print('이전 화면으로 돌아갑니다');break 
                            elif check==False: print(f'{choice_ing}는 올바르지 않은 번호입니다.');continue
                            else: print(f'{choice_ing}는 올바르지 않은 번호입니다.');continue
                    elif extra== 3:
                        print('메뉴 화면으로 돌아갑니다');break 
                    elif extra==4:
                        while True:
                            print_set()
                            choice_set=input('세트 여부를 선택해 주세요')   #인풋6. 세트 여부//
                            check=True
                            if data_chek(choice_set):
                                choice_set= int(choice_set)
                            else: check=False            
                            if choice_set==1:
                                burger.price += 2000  
                                print(f"{burger.burger_name} 세트 (+2000원)\n")
                                menu_set=True
                                break
                            elif choice_set==2:
                                print(f"{burger.burger_name} 단품.\n")
                                menu_set=False
                            elif check==False: print(f'{choice_set}는 올바르지 않은 번호입니다.');continue
                            else: print(f'{choice_set}는 올바르지 않은 번호입니다.');continue
                            
                            # order.append(burger)    
                            break
                        while True:
                            print_take()
                            choice_take=input('주문 방식을 선택해 주세요')  #인풋7. 주문 방식//
                            check=True
                            if data_chek(choice_take):
                                choice_take= int(choice_take)
                            else: check=False            
                            if choice_take==1:
                                take=['포장'];break
                            elif choice_take==2:
                                take=['매장 식사'];break
                            elif check==False:print(f'{choice_take}는 올바르지 않은 번호입니다.');continue
                            else: print(f'{choice_take}는 올바르지 않은 번호입니다.');continue
                        while True:
                            print_pay()
                            choice_pay=input('결제 방식을 선택해 주세요')  #인풋8. 결제 방식//
                            check=True
                            if data_chek(choice_pay):
                                choice_pay= int(choice_pay)
                            else: check=False            
                            if choice_pay==1:
                                pay=['카드'];break
                            elif choice_pay==2:
                                pay=['현금'];break
                            elif check==False:print(f'{choice_pay}는 올바르지 않은 번호입니다.');continue
                            else: print(f'{choice_pay}는 올바르지 않은 번호입니다.');continue

                        while True:
                            print_reciept()
                            choice_reciept= input('영수증 출력 여부를 선택해 주세요')  #인풋9. 영수증 여부//
                            check=True
                            if data_chek(choice_reciept):
                                choice_reciept= int(choice_reciept)
                            else: check=False            
                            if choice_reciept==1:
                                receipt= True;break
                            elif choice_reciept==2:
                                receipt= False;break
                            elif check==False:print(f'{choice_reciept}는 올바르지 않은 번호입니다.')
                            else:print(f'{choice_reciept}는 올바르지 않은 번호입니다.')
                        while True:
                            order.append(burger) 
                            if receipt:
                                print('주문 내역')
                                for burger in order:
                                    burger.display_info()
                                print(f'*번호표*\n {x}번\n주문방식:{take}\n결제방식: {pay}' )
                            else:
                                print(f'*번호표*\n {x}번\n주문방식:{take}\n결제방식: {pay}' )

                            print('이용해 주셔서 감사합니다')
                            input()
                            x+=1
                            reset=True
                            break  
                    elif check==False: print(f'{extra}는 올바르지 않은 번호입니다.');continue
                    else: print(f'{extra}는 올바르지 않은 번호입니다.');continue        
                    if reset: break       
                if reset: break
            if reset: break    
    elif check==False: print(f'{choice_main}은 올바른 번호가 아닙니다') 
    else: print(f'{choice_main}은 올바른 번호가 아닙니다')            
                    

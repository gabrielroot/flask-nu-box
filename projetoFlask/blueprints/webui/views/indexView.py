from flask import render_template
from flask_login import login_required, current_user
from projetoFlask.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from projetoFlask.blueprints.webui.repository.TransactionRepository import TransactionRepository
from projetoFlask.blueprints.webui.repository.BoxRepository import BoxRepository
from projetoFlask.blueprints.webui.repository.BalanceRepository import BalanceRepository

@login_required
def index():
    transactions = TransactionRepository.findMyActivesTransactions(current_user).limit(10)

    sum_of_deposits_from_boxes = TransactionRepository.sumOfWithdrawsOrDepositsFromBoxes(current_user, TransactionOperation.DEPOSIT.name)
    sum_of_withdraws_from_boxes = TransactionRepository.sumOfWithdrawsOrDepositsFromBoxes(current_user, TransactionOperation.WITHDRAW.name)
    total_in_boxes = BoxRepository.getSumOfValuesInBoxes(current_user=current_user)
    all_summation = BalanceRepository.getAllSummation(current_user=current_user)
    count_all_goal_boxes = BoxRepository.countAllGoalBoxes(current_user=current_user)
    
    dashboard = dict(
        sum_of_deposits_from_boxes = sum_of_deposits_from_boxes,
        sum_of_withdraws_from_boxes = sum_of_withdraws_from_boxes,
        total_in_boxes = total_in_boxes, 
        all_summation = all_summation, 
        count_all_goal_boxes = count_all_goal_boxes
    )
    
    return render_template("dashboard.html", items=transactions, operation=TransactionOperation, dashboard=dashboard)
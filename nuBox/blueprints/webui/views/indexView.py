from flask import render_template
from flask_login import login_required, current_user
from nuBox.blueprints.webui.repository.BoxRepository import BoxRepository
from nuBox.blueprints.webui.repository.BalanceRepository import \
    BalanceRepository
from nuBox.blueprints.webui.repository.TransactionRepository import \
    TransactionRepository
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


@login_required
def index():
    pagination = TransactionRepository.\
        findMyActivesTransactions(current_user).paginate(page=1, per_page=3)

    count_transactions_in_boxes_by_week_day = TransactionRepository.\
        countTransactionsInBoxesByWeekDay(current_user=current_user)
    sum_of_deposits_from_boxes = TransactionRepository.\
        sumOfWithdrawsOrDepositsFromBoxes(
            current_user,
            TransactionOperation.DEPOSIT.name
        )
    sum_of_withdraws_from_boxes = TransactionRepository.\
        sumOfWithdrawsOrDepositsFromBoxes(
            current_user,
            TransactionOperation.WITHDRAW.name
        )
    total_in_boxes = BoxRepository.\
        getSumOfValuesInBoxes(current_user=current_user)
    all_summation = BalanceRepository.\
        getAllSummation(current_user=current_user)
    count_all_goal_boxes = BoxRepository.\
        countAllGoalBoxes(current_user=current_user)

    dashboard = dict(
        sum_of_deposits_from_boxes=sum_of_deposits_from_boxes,
        sum_of_withdraws_from_boxes=sum_of_withdraws_from_boxes,
        total_in_boxes=total_in_boxes,
        all_summation=all_summation,
        count_all_goal_boxes=count_all_goal_boxes,
        count_transactions_in_boxes_by_week_day=count_transactions_in_boxes_by_week_day
    )

    return render_template("dashboard.html", pagination=pagination,
                           operation=TransactionOperation, dashboard=dashboard
                           )

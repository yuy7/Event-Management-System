from flask import request, jsonify, session
from __init__ import db
from Dao.Budget import Budget, BudgetApp
from Dao.Event import Event
from sqlalchemy import and_

from Dao.UserAddEvent import UserAddEvent

from Dao.UserEvent import UserEvent


def set_budget():
    try:
        data = request.get_json()
        eventID = data.get('eventID')
        if not eventID:
            return jsonify({"error": "eventID is required"})

        # 检查是否已经存在相同 eventID 的预算
        existing_budget = Budget.query.filter_by(eventID=eventID).first()
        if existing_budget:
            return jsonify({"error": "Budget for this event already exists"}), 200

        new_budget = Budget(
            eventID=eventID,
            userID=data.get('userID'),
            initialBudget=data.get('initialBudget'),
            actualCost=data.get('actualCost')
        )
        db.session.add(new_budget)
        db.session.commit()
        return jsonify({"status": "Budget set successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_event_by_user():
    try:
        user_id = request.args.get('userid')
        if not user_id:
            return jsonify({"error": "userid is required"}), 400

        result = Event.query.filter(and_(Event.reservationUserId == user_id, Event.budget == None)).all()
        return jsonify({"result": [
            {'id': r.eventID, 'name': r.eventName} for r in result
        ]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_event_by_app_user():
    try:
        user_id = request.args.get('userid')
        if not user_id:
            return jsonify({"error": "userid is required"}), 400

        #
        ids1 = UserAddEvent.query.filter(and_(UserAddEvent.userID == user_id, UserAddEvent.state == 1)).all()

        print(user_id)

        ids2 = UserEvent.query.filter(UserEvent.userID == user_id).all()
        # ids2 = UserEvent.query.filter().all()

        print(ids2)

        ids = []
        for _id in ids1:
            ids.append(_id.eventID)
        for _id in ids2:
            ids.append(_id.eventID)

        # ids = [1]

        print(ids)

        result = Event.query.filter(and_(Event.eventID.in_(ids), Event.budget != None)).all()
        return jsonify({"result": [
            {'id': r.eventID, 'name': r.eventName, 'surplus': float(r.budget.initialBudget)-float(r.budget.actualCost)}
            for r in result
        ]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_budget():
    try:
        if request.method == 'GET':
            budgets = Budget.query.all()
            result = [
                {
                    "budgetID": budget.budgetID,
                    "eventID": budget.eventID,
                    # "userID": budget.userID,
                    "e_name": budget.event.eventName,
                    "initialBudget": budget.initialBudget,
                    "actualCost": budget.actualCost,
                    "createdAt": budget.createdAt,
                    "updatedAt": budget.updatedAt
                }
                for budget in budgets
            ]
            return jsonify(result), 200

        elif request.method == 'PUT':
            data = request.get_json()
            actualCost = data.get('actualCost')
            initialBudget = data.get('initialBudget')
            eventID = data.get('eventID')

            # 检查是否已经存在相同 eventID 的预算
            existing_budget = Budget.query.filter_by(eventID=eventID).first()
            if existing_budget:
                return jsonify({"error": "Budget for this event already exists"}), 200

            budget = Budget(
                initialBudget=initialBudget,
                actualCost=actualCost,
                eventID=eventID
            )

            db.session.add(budget)
            db.session.commit()
            return jsonify({"message": "新增成功"}), 201

        elif request.method == 'PATCH':
            data = request.get_json()
            budgetID = data.get('budgetID')
            actualCost = data.get('actualCost')
            initialBudget = data.get('initialBudget')

            Budget.query.filter_by(budgetID=budgetID).update(
                {Budget.actualCost: actualCost, Budget.initialBudget: initialBudget}
            )
            db.session.commit()
            return jsonify({"message": "修改成功"}), 200

        elif request.method == 'POST':
            data = request.get_json()
            budgetID = data.get('budgetID')
            print(budgetID)

            if not budgetID:
                return jsonify({"error": "budgetID is required"}), 400

            budget = Budget.query.filter_by(budgetID=budgetID).first()
            if not budget:
                return jsonify({"error": "Budget not found"}), 404

            db.session.delete(budget)
            db.session.commit()
            return jsonify({"message": "删除成功"}), 200

        else:
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_budget_app():
    if request.method == 'GET':
        budget_apps = BudgetApp.query.all()
        result = [
            {
                "BudgetAppID": budget_app.BudgetAppID,
                "e_name": budget_app.event.eventName,
                "e_user": budget_app.event.reservationUserId,
                "cost": budget_app.cost,
                "u_name": budget_app.user.Username,
                "status": budget_app.status
            }
            for budget_app in budget_apps
        ]
        return jsonify(result), 200
    elif request.method == 'PUT':
        data = request.get_json()
        cost = data.get('cost')
        userID = data.get('userID')
        eventID = data.get('eventID')

        # print(cost,userID,eventID)

        budget_app = BudgetApp(
            cost=cost,
            userID=userID,
            eventID=eventID,
            status='待审批'
        )
        db.session.add(budget_app)
        db.session.commit()
        return jsonify({"message": "新增成功"}), 201

    elif request.method == 'PATCH':
        data = request.get_json()
        budgetAppID = data.get('budgetAppID')
        status = data.get('status')

        budget_app = BudgetApp.query.filter_by(BudgetAppID=budgetAppID).first()
        BudgetApp.query.filter_by(BudgetAppID=budgetAppID).update(
            {BudgetApp.status: status}
        )
        db.session.commit()

        # 如果审批通过，修改预算表实际花费
        if status == '审批通过':
            budget_id = BudgetApp.query.filter_by(BudgetAppID=budgetAppID).first().event.budget
            budget = Budget.query.filter_by(budgetID=budget_id.budgetID).first()
            # print(budget)
            Budget.query.filter_by(budgetID=budget_id.budgetID).update(
                {Budget.actualCost: float(budget.actualCost)+float(budget_app.cost)}
            )
            db.session.commit()
        return jsonify({"message": "审批成功"}), 200

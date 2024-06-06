from flask import request, jsonify

from __init__ import db
from Dao.Budget import Budget


def set_budget():
    data = request.get_json()
    new_budget = Budget(
        eventID=data['eventID'],
        userID=data['userID'],
        initialBudget=data['initialBudget'],
        actualCost=data['actualCost']
    )
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({"status": "Budget set successfully"}), 201


def get_budget():
    if request.method == 'GET':
        budgets = Budget.query.all()
        result = [
            {
                "budgetID": budget.budgetID,
                # "eventID": budget.eventID,
                # "userID": budget.userID,
                "initialBudget": budget.initialBudget,
                "actualCost": budget.actualCost,
                "createdAt": budget.createdAt,
                "updatedAt": budget.updatedAt
            }
            for budget in budgets
        ]
        return jsonify(result), 200
    elif request.method == 'PUT':
        actualCost = request.json.get('actualCost')
        initialBudget = request.json.get('initialBudget')
        budget = Budget()
        budget.initialBudget = initialBudget
        budget.actualCost = actualCost
        db.session.add(budget)
        db.session.commit()
        return {"message": "新增成功"}
    elif request.method == 'PATCH':
        budgetID = request.json.get('budgetID')
        actualCost = request.json.get('actualCost')
        initialBudget = request.json.get('initialBudget')
        Budget.query.filter_by(budgetID=budgetID).update({Budget.actualCost:actualCost,Budget.initialBudget:initialBudget})
        db.session.commit()
        return {"message": "修改成功"}
    else:
        budgetID = request.json.get('budgetID')
        # print()
        print(budgetID)
        db.session.delete(Budget.query.filter_by(budgetID=budgetID).first())
        db.session.commit()
        return jsonify({"message": "删除成功"})

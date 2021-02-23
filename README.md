# flask-rest-api
Link: http://107.178.212.44

# Endpoint: 

## method = ['GET', 'POST', 'PUT', 'DELETE']
- /api/v1/customer/*(customerNumber)
- /api/v1/employee/*(employeeNumber)
- /api/v1/office/*(officeCode)
- /api/v1/orderdetail/*(orderNumber or productCode)
- /api/v1/order/*(orderNumber)
- /api/v1/payment/*(customerNumber)
- /api/v1/productline/*(productLine)
- /api/v1/product/*(productCode)

## GET list of data
- /api/v1/customers # filter_by: country, customerNumber # sort_by any field
- /api/v1/employees # filter_by: firstName, reportsTo # sort_by any field
- /api/v1/offices # filter_by: city, phone # sort_by any field
- /api/v1/orderdetails # filter_by: productCode, quantityOrdered # sort_by any field
- /api/v1/orders # filter_by: orderDate, requiredDate # sort_by any field
- /api/v1/payments # filter_by: paymentDate, checkNumber # sort_by any field
- /api/v1/productlines # filter_by: textDescription, htmlDescription # sort_by any field
- /api/v1/products # filter_by: productName, productLine # sort_by any field

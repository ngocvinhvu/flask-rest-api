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
- /api/v1/productline/*(productLine) (must get token for authentication with default username and password is admin)
- /api/v1/product/*(productCode)

## GET list of data
- /api/v1/customers # filter_by: country, customerNumber # sort_by any field
- /api/v1/employees # filter_by: jobTitle, officeCode # sort_by any field
- /api/v1/offices # filter_by: country, city # sort_by any field
- /api/v1/orderdetails # filter_by: quantityOrdered, orderNumber # sort_by any field
- /api/v1/orders # filter_by: customerNumber, orderNumber # sort_by any field
- /api/v1/payments # filter_by: customerNumber, paymentDate # sort_by any field
- /api/v1/productlines # filter_by: productLine # sort_by any field
- /api/v1/products # filter_by: productCode, productLine # sort_by any field


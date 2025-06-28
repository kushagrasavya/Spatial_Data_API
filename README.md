Use uvicorn main:app --reload in the main directory with the requirements pre-installed.

*FEW ASSUMPTIONS THAT I MADE*

1. There might be cases where users need to delete a specific point. To support this, I implemented a DELETE API endpoint that allows points and polygons to be removed by their name.

2. To enable precise data retrieval, I included GET endpoints that allow fetching individual points or polygons using their unique MongoDB Object ID.
   
3. A description field has been added to the point model, allowing users to include additional information or context about a specific location.
   
4. A colour field has been included in the polygon model to support visual distinction when rendering polygons on a map or UI, making the data more engaging and easier to interpret.

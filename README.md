# My shops

## Generalities
The web app allows a user to :
- create an account
- login/logout
- dislike some shops which hides them for 2 hours
- display the list of shops near his location
- like some shops and see them on the *My Preferred Shops* page
- remove a shop from the list of liked shops

## Technical discussion
I used a [another personal project](https://github.com/jamalg/my_notes) to bootstrap *My Shops*. You can refer to the [Generalities](https://github.com/jamalg/my_notes#generalities) section of that project for details about the architecture and technology choices.

### Python backend:
- **Flask** app to RESTfully serve resources
- **SQLAlchemy** + **Postgres** as a database
- **Alembic** to handle schema migrations
- **Marshamallow** for serialization/deserialization
- Some patterns:
    - As recommended by the *Twelve Factor App* config is stored in environment variables. The conlig class in `back.utils.config_class.config::BaseConfig` leverages the power of Python descriptors to make declaring and managing configuration easier. See `back.config.py`
    - Minimal checkout pattern for database operation : Try to open the connection at last moment and close it as soon as possible. See usage of `utils.sqlalchemy.helpers::session_manager` in `models.helper::add_one`
    - The scope of the session is tied to the request cycle. The usage of `scopefunc=_app_ctx_stack.__ident_func__` in `models.db::session` and the callback attached to `app.teardown_request` in `back.models.__init__::init_app` makes the API sustain a much larger charge load. You get all these benefits and more by using **FlaskSQLALchemy** but sometimes it's also good to be aware of what is happening
    - When possible functions and helpers are written to promote intention and make reading application code easier. The philosophy is that application code in API routes or scripts should do `helper.add_user(user_data)` rather than `helper.add_one(user_data, UserSchema)`

### Reactjs frontend:
- **Redux** for state management : some of the opinionated best practices proposed in the documentation are followed
    - central definition of action types `front/src/defs.js`
    - helper is used to make writing of simple action creators simpler `front/src/redux/actions/utils.js::makeCreators`
    - reducers composition
- **Immutable.js** as support for the state :
    - Guaranteed immutabily, leveraging full potential of shallow equality test
    - Usage of [withImmutablePropsToJS](https://github.com/tophat/with-immutable-props-to-js) to keep dump components as dump as possible. See containers in `front/src/containers`
- **Normalizr**: this really is a productivity boost
    - A single action is dispatched to handle all entities. Adding other resources should only require three main steps + some caution
        - define a new schema in `front/src/schemas.js`
        - add a reducer that handles `defs.ADD_ENTITIES`
        - write the async function that make the API call like `front/src/redux/async.js::fetchFolder`
        - *Noted that some caution needs to be observed because the state is an immutable object*. If the merge is done not properly it can lead to some unexpected behavior 
- When needed Higher Order Components are used :
    - Example with `withStatusBouncer` in `front/src/containers/statusBouncer.js`

### Cross concern
- Shops nearby and details about them are obtained using [GooglePlaceApi](https://developers.google.com/places/web-service/intro). I chose not to store
Places objects in the database mainly because it involved to solve the classic update and refresh issues inherent to maintaining a copy of an external database. Nevertheless, the API is cached to mitigate the performance cost of not having data locally.
- Dislikes are stored in the main database but contrary to Redis, PostgreSQL doesn't come up with out of the box support for an expiry feature. Only using active
dislike is done at the application level by using the `User.fresh_dilikes` property. Then there is a command script to purge old dislikes. Calling this script every deploy seemed less costly than having an SQLALchemy trigger or listener that does this after every commit for example.

## How to boot up the app

### Environment variables
The app expects a `.env` and `prod.env` files with environment variables. A comprehensive example with default values is given in `env.example`.
```bash
# Create environment file
cat env.example >> .env
```
**Note that you need a *GOOGLE_CLOUD_API_KEY* with access to the *Place API* enabled for the backend to work**. Of course there is a free tier scheme.

### Build, Up, Bootup
These commands should get you up and running for dev. The production `docker-compose` uses Dockerfiles that are optimized (no install of dev dependencies, different nginx configuration, `npm build` rather then `npm start` )
```bash
make build
make up
make upgrade # Create model tables
```
Check that the back API is working well at `http://localhost/api/status`. Front should be served at `http://localhost`.

**Note that for production build and deploy** you need to update the value of `REACT_APP_API_URL` directly in `docker-compose-prod.yml` as it's needed at built time.

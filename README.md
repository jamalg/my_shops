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

I add here only what is specific to this project:
- Shops nearby and details about them are obtained using [GooglePlaceApi](https://developers.google.com/places/web-service/intro). It chose not to store
Places objects in the back end database mainly because it involved to solve the classic update and refresh issues inherent to maintaining a copy of an external database. Nevertheless, the API is cached to mitigate the performance cost of not having data locally.
- Dislikes are stored in the main database but contrary to Redis, PostgreSQL doesn't come up with out of the box support for an expiry feature. Only using active
dislike is done at the application level by using the `User.fresh_dilikes` property. Then there is a command script to purge old dislikes. Calling this script every deploy seemed less costly than having an SQLALchemy trigger or listener that does this after every commit for example.
- There some work left to do on configuring the Nginx that serves the front assets in `front/docker/Dockerfile-prod`. The issue is that if you navigate to the prod url then to `/nearby` it works but not if you navigate directly to `/nearby` withou loading the React app first.

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
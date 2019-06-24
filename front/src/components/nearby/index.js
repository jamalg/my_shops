import { Nearby } from './component'
import { withStatusBouncer } from '../../containers/statusBouncer'
import { withLoginBouncer } from '../../containers/loginBouncer'
import { withLocationBouncer } from '../../containers/locationBouncer'

export default withLoginBouncer(withLocationBouncer(withStatusBouncer(Nearby)))

import { Liked } from './component'
import { withStatusBouncer } from '../../containers/statusBouncer'
import { withLoginBouncer } from '../../containers/loginBouncer'

export default withLoginBouncer(withStatusBouncer(Liked))

# 3. Class diagram

UML class diagram of the Public Module, split into three views so it stays readable. The complete diagram, with every class together, is in the annex (section 3.5).

How to read it:

- Classes with the `«read-only»` stereotype are projections of the tournament-management platform (through the `public_*` views). Every other class is owned by this module.
- Classes with a **dashed border** are defined in another view and are repeated only to show how this view connects to the rest. Their stereotype says which view that is.
- `«PK»` marks the primary key and `«FK»` a foreign key, so every relationship can be traced to its column in section 4.
- Visibility: `+` public, `-` private.

<div class="landscape">

## 3.1 Competition (read-only projection)

```mermaid
---
config:
  layout: elk
---
classDiagram
  direction LR
  class Organization {
    <<read-only>>
    +id: UUID «PK»
    +name: String
    +slug: String
    +logoUrl: String
    +primaryColor: String
    +secondaryColor: String
  }
  class Tournament {
    <<read-only>>
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +name: String
    +slug: String
    +startDate: Date
    +endDate: Date
    +isPublic: Boolean
    +categories() List~Category~
  }
  class Category {
    <<read-only>>
    +id: UUID «PK»
    +tournamentId: UUID «FK»
    +name: String
    +order: Int
    +groups() List~Group~
  }
  class Group {
    <<read-only>>
    +id: UUID «PK»
    +categoryId: UUID «FK»
    +name: String
    +standings() List~Standing~
  }
  class Matchday {
    <<read-only>>
    +id: UUID «PK»
    +tournamentId: UUID «FK»
    +categoryId: UUID «FK»
    +number: Int
    +name: String
    +startDate: Date
    +endDate: Date
    +matches() List~Match~
  }
  class Club {
    <<read-only>>
    +id: UUID «PK»
    +name: String
    +logoUrl: String
    +teamsByCategory(t: Tournament) Map
  }
  class Team {
    <<read-only>>
    +id: UUID «PK»
    +clubId: UUID «FK»
    +categoryId: UUID «FK»
    +groupId: UUID «FK»
    +name: String
    +slug: String
    +isWithdrawn: Boolean
    +upcomingMatches() List~Match~
    +recentResults() List~Match~
    +currentPosition() Int
  }
  class Venue {
    <<read-only>>
    +id: UUID «PK»
    +tournamentId: UUID «FK»
    +name: String
    +address: String
  }
  class Field {
    <<read-only>>
    +id: UUID «PK»
    +venueId: UUID «FK»
    +name: String
  }
  class Match {
    <<read-only>>
    +id: UUID «PK»
    +matchdayId: UUID «FK»
    +groupId: UUID «FK»
    +homeTeamId: UUID «FK»
    +awayTeamId: UUID «FK»
    +fieldId: UUID «FK»
    +kickoff: DateTime
    +status: MatchStatus
    +homeGoals: Int
    +awayGoals: Int
    +publicStatus() PublicStatus
    +isBookable() Boolean
  }
  class Goal {
    <<read-only>>
    +id: UUID «PK»
    +matchId: UUID «FK»
    +teamId: UUID «FK»
    +playerName: String
    +quantity: Int
    +ownGoal: Boolean
  }
  class Standing {
    <<read-only>>
    +groupId: UUID «PK, FK»
    +teamId: UUID «PK, FK»
    +position: Int
    +played: Int
    +won: Int
    +drawn: Int
    +lost: Int
    +goalsFor: Int
    +goalsAgainst: Int
    +points: Int
    +hasProvisional: Boolean
    +goalDifference() Int
  }
  class Document {
    <<read-only>>
    +id: UUID «PK»
    +tournamentId: UUID «FK»
    +title: String
    +type: String
    +publishedAt: DateTime
    +fileUrl: String
  }
  class PublicStatus {
    <<enumeration>>
    TO_BE_SCHEDULED
    SCHEDULED
    PROVISIONAL
    FINAL
    POSTPONED
    WALKOVER
  }

  Organization "1" *-- "0..*" Tournament
  Tournament "1" *-- "1..*" Category
  Tournament "1" *-- "0..*" Matchday
  Tournament "1" *-- "0..*" Venue
  Tournament "1" *-- "0..*" Document
  Category "1" *-- "0..*" Group
  Category "0..1" o-- "0..*" Matchday
  Club "1" o-- "1..*" Team
  Category "1" o-- "0..*" Team
  Group "1" o-- "2..*" Team
  Venue "1" *-- "1..*" Field
  Matchday "0..1" o-- "0..*" Match
  Group "0..1" o-- "0..*" Match
  Match "0..*" --> "1" Team : home
  Match "0..*" --> "1" Team : away
  Match "0..*" --> "0..1" Field
  Match "1" *-- "0..*" Goal
  Goal "0..*" --> "1" Team
  Group "1" *-- "0..*" Standing
  Standing "0..*" --> "1" Team
  Match ..> PublicStatus
```

</div>

<div class="landscape">

## 3.2 Public site, fans and content

```mermaid
---
config:
  layout: elk
---
classDiagram
  direction LR
  class PublicSite {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +customDomain: String
    +logoUrl: String
    +primaryColor: String
    +secondaryColor: String
    +sections: SectionFlags
    +publishTournament(t: Tournament) void
    +toggleSection(s: Section, on: Boolean) void
    +manifest() WebManifest
  }
  class PublishedTournament {
    +siteId: UUID «PK, FK»
    +tournamentId: UUID «PK, FK»
    +publishedAt: DateTime
  }
  class Organization:::reference {
    <<read-only, see 3.1>>
  }
  class Tournament:::reference {
    <<read-only, see 3.1>>
  }
  class Team:::reference {
    <<read-only, see 3.1>>
  }
  class Match:::reference {
    <<read-only, see 3.1>>
  }
  class Matchday:::reference {
    <<read-only, see 3.1>>
  }
  class User {
    <<abstract>>
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +email: String
    +displayName: String
    +role: Role
    +signIn() Session
  }
  class FanAccount {
    +authProvider: String
    +adultConfirmedAt: DateTime
    +follow(t: Team) TeamFollow
    +unfollow(t: Team) void
    +myTeams() List~Team~
  }
  class OrganizerAccount
  class PhotographerAccount {
    +assignedMatches() List~Match~
  }
  class SponsorAccount
  class TeamFollow {
    +accountId: UUID «PK, FK»
    +teamId: UUID «PK, FK»
    +createdAt: DateTime
  }
  class PushSubscription {
    +id: UUID «PK»
    +accountId: UUID «FK»
    -endpoint: String
    -p256dh: String
    -auth: String
    +active: Boolean
    +lastOkAt: DateTime
    +deactivate() void
  }
  class Notification {
    +id: UUID «PK»
    +accountId: UUID «FK»
    +matchId: UUID «FK»
    +type: NotificationType
    +title: String
    +body: String
    +url: String
    +pushSentAt: DateTime
    +readAt: DateTime
    +send() void
    +markAsRead() void
  }
  class NewsPost {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +authorId: UUID «FK»
    +title: String
    +body: String
    +coverUrl: String
    +tag: String
    +status: PostStatus
    +publishedAt: DateTime
    +publish() void
  }
  class GalleryPhoto {
    +id: UUID «PK»
    +postId: UUID «FK»
    +matchdayId: UUID «FK»
    +imageUrl: String
    +caption: String
  }
  class Widget {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +type: WidgetType
    +options: JSON
    +embedCode() String
  }

  Organization "1" -- "1" PublicSite
  PublicSite "1" *-- "0..*" PublishedTournament
  PublishedTournament "0..*" --> "1" Tournament
  Organization "1" *-- "0..*" User
  User <|-- FanAccount
  User <|-- OrganizerAccount
  User <|-- PhotographerAccount
  User <|-- SponsorAccount
  FanAccount "1" *-- "0..*" TeamFollow
  TeamFollow "0..*" --> "1" Team
  User "1" *-- "0..*" PushSubscription
  User "1" *-- "0..*" Notification
  Notification "0..*" --> "0..1" Match : about
  Organization "1" *-- "0..*" NewsPost
  OrganizerAccount "1" --> "0..*" NewsPost : writes
  NewsPost "1" *-- "0..*" GalleryPhoto
  GalleryPhoto "0..*" --> "0..1" Matchday
  Organization "1" *-- "0..*" Widget
  OrganizerAccount ..> PublicSite : manages

  classDef reference fill:#f7f7f7,stroke:#888,stroke-dasharray:5 4
```

</div>

## 3.3 Sponsorship and commerce

### a) Sponsorship

```mermaid
---
config:
  layout: elk
---
classDiagram
  direction LR
  class Sponsor {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +accountId: UUID «FK»
    +name: String
    +logoUrl: String
    +contactEmail: String
    +metrics(from: Date, to: Date) MetricsReport
  }
  class SponsorPlacement {
    +id: UUID «PK»
    +sponsorId: UUID «FK»
    +slot: PlacementSlot
    +creativeUrl: String
    +targetUrl: String
    +startDate: Date
    +endDate: Date
    +isActive(today: Date) Boolean
    +recordImpression() void
    +recordClick() void
  }
  class PlacementEvent {
    +id: BigInt «PK»
    +placementId: UUID «FK»
    +type: EventType
    +occurredAt: DateTime
    +channel: String
  }
  class Organization:::reference {
    <<read-only, see 3.1>>
  }
  class SponsorAccount:::reference {
    <<see 3.2>>
  }
  Organization "1" *-- "0..*" Sponsor
  SponsorAccount "0..1" -- "0..1" Sponsor : logs in as
  Sponsor "1" *-- "0..*" SponsorPlacement
  SponsorPlacement "1" *-- "0..*" PlacementEvent

  classDef reference fill:#f7f7f7,stroke:#888,stroke-dasharray:5 4
```

<div class="landscape">

### b) Store, photo/video bookings, payments and pre-registrations

```mermaid
---
config:
  layout: elk
---
classDiagram
  direction LR
  class Product {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +name: String
    +description: String
    +photoUrl: String
    +price: Money
    +active: Boolean
  }
  class ProductVariant {
    +id: UUID «PK»
    +productId: UUID «FK»
    +size: String
    -stock: Int
    +reserve(qty: Int) void
  }
  class Order {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +accountId: UUID «FK»
    +number: String
    +status: OrderStatus
    +total: Money
    +addItem(v: ProductVariant, qty: Int) void
    +checkout() Payment
    +markReady() void
    +markDelivered() void
  }
  class OrderItem {
    +orderId: UUID «PK, FK»
    +variantId: UUID «PK, FK»
    +quantity: Int
    +unitPrice: Money
    +subtotal() Money
  }
  class Payment {
    +id: UUID «PK»
    +orderId: UUID «FK»
    +bookingId: UUID «FK»
    -gatewayRef: String
    +amount: Money
    +status: PaymentStatus
    -rawEvent: JSON
    +confirmedAt: DateTime
    +applyWebhook(e: GatewayEvent) void
  }
  class MediaPackage {
    +id: UUID «PK»
    +organizationId: UUID «FK»
    +name: String
    +type: MediaType
    +price: Money
    +bookingCutoffHours: Int
    +active: Boolean
  }
  class MediaAvailability {
    +packageId: UUID «PK, FK»
    +matchdayId: UUID «PK, FK»
    +capacity: Int
    +remainingSlots() Int
  }
  class MediaBooking {
    +id: UUID «PK»
    +accountId: UUID «FK»
    +matchId: UUID «FK»
    +packageId: UUID «FK»
    +status: BookingStatus
    +unitPrice: Money
    +expiresAt: DateTime
    +deliveryUrl: String
    +deliveredAt: DateTime
    +deliver(url: String) void
  }
  class PhotographerAssignment {
    +matchId: UUID «PK, FK»
    +photographerId: UUID «FK»
    +assignedBy: UUID «FK»
    +assignedAt: DateTime
  }
  class PreRegistration {
    +id: UUID «PK»
    +tournamentId: UUID «FK»
    +reviewedBy: UUID «FK»
    +clubName: String
    +contactName: String
    +contactEmail: String
    +contactPhone: String
    +categories: List~String~
    +status: ReviewStatus
    +reason: String
    +approve() void
    +reject(reason: String) void
  }
  class Organization:::reference {
    <<read-only, see 3.1>>
  }
  class Tournament:::reference {
    <<read-only, see 3.1>>
  }
  class Matchday:::reference {
    <<read-only, see 3.1>>
  }
  class Match:::reference {
    <<read-only, see 3.1>>
  }
  class FanAccount:::reference {
    <<see 3.2>>
  }
  class OrganizerAccount:::reference {
    <<see 3.2>>
  }
  class PhotographerAccount:::reference {
    <<see 3.2>>
  }
  class PaymentGateway {
    <<interface>>
    +createCheckout(p: Payment) URL
    +verifySignature(e: GatewayEvent) Boolean
  }

  Organization "1" *-- "0..*" Product
  Product "1" *-- "1..*" ProductVariant
  Organization "1" --> "0..*" Order
  FanAccount "1" --> "0..*" Order
  Order "1" *-- "1..*" OrderItem
  OrderItem "0..*" --> "1" ProductVariant
  Order "1" --> "0..*" Payment
  Organization "1" *-- "0..*" MediaPackage
  MediaPackage "1" *-- "0..*" MediaAvailability
  MediaAvailability "0..*" --> "1" Matchday
  Matchday "0..1" o-- "0..*" Match
  FanAccount "1" --> "0..*" MediaBooking
  MediaBooking "0..*" --> "1" Match
  MediaBooking "0..*" --> "1" MediaPackage
  MediaBooking "1" --> "0..*" Payment
  Match "1" -- "0..1" PhotographerAssignment
  PhotographerAssignment "0..*" --> "1" PhotographerAccount
  OrganizerAccount "1" --> "0..*" PhotographerAssignment : assigns
  Organization "1" *-- "0..*" Tournament
  PreRegistration "0..*" --> "1" Tournament
  OrganizerAccount "0..1" --> "0..*" PreRegistration : reviews
  Payment ..> PaymentGateway : uses

  classDef reference fill:#f7f7f7,stroke:#888,stroke-dasharray:5 4
```

</div>

## 3.4 Design notes

- **Read-only projection.** Competition classes have no mutating methods in this module: the management platform owns them (Domain-Driven Design *bounded context*). The Public Module talks to them only through views, which keeps the dependency one-way.
- **Two catalogues, because they sell different things.** `Product` and `ProductVariant` are the store: physical merchandise such as a jersey, which has sizes and a stock per size (RF-22). `MediaPackage` holds the photo and video plans a fan can choose, with their price (RF-25). These plans have no size, and their limit is not a stock: it depends on the matchday, so it lives in `MediaAvailability`.
- **Capacity per matchday.** `MediaAvailability` is the association between a `MediaPackage` and a `Matchday`, and holds how many bookings that package accepts on that matchday (BR-19). A `MediaBooking` points to a `Match`, and the match gives the matchday. That is the path used to count the slots taken.
- **Fields are not booked.** `Venue` and `Field` stay in the model because each match must say where it is played (RF-01, HU-31). No class books them (BR-17).
- **Dependency inversion.** `Payment` depends on the `PaymentGateway` interface, not on a concrete provider, so the gateway can change without touching orders or bookings (SOLID: DIP and OCP).
- **Single responsibility.** `Notification` only builds and delivers messages; deciding *who* gets them belongs to `TeamFollow`; computing standings stays in the platform's `Standing` view.
- **Roles by specialization.** `FanAccount`, `OrganizerAccount`, `PhotographerAccount` and `SponsorAccount` specialize `User`. In the database this becomes one `pm_accounts` table linked to the authentication provider (`auth.users`) with a `role` column (see section 4).

## 3.5 Annex: complete class diagram

The three views above are one model, split only for reasons of space. The annex shows every class and relationship together:

- [annex/Workshop-2-class-diagram-annex.pdf](annex/Workshop-2-class-diagram-annex.pdf): the complete diagram on a single large page.
- [annex/class-diagram-full.drawio.xml](annex/class-diagram-full.drawio.xml): the same diagram as an editable XML file, which opens in [diagrams.net](https://app.diagrams.net/).
